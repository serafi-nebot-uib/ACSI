#!/usr/bin/env python3

from __future__ import annotations

import re
import time
import subprocess
from pathlib import Path

TIME_UNITS = { "h": 60*60, "m": 60, "s": 1, "ms": 1/1000, "us": 1/1000000 }

def cpu() -> tuple[float, float]:
  with Path("/proc/stat").open("r") as f:
    # field order: [user] [nice] [system] [idle] [iowait] [irq] [softirq] [steal] [guest] [guest_nice]
    fields = list(map(int, f.readline().strip().split()[1:]))
    return sum(fields), fields[3] + fields[4]

def mem() -> tuple[float, float]:
  with Path("/proc/meminfo").open("r") as f:
    return tuple(float(f.readline().split()[1].split()[0]) * 1024 for _ in range(3))

def load(*, num_threads: int, max_prime: int, monitor_interval: float, print_overhead: int = False) -> tuple[float, list[float], list[float]]:
  cmd = ["sysbench", f"--num-threads={num_threads}", "--test=cpu", f"--cpu-max-prime={max_prime}", "run"]
  cpu_prev, time_start = cpu(), time.time()
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa: S603

  cpu_usage, mem_usage = [], []
  while True:
    time_total = time.time() - time_start
    sleep_time = monitor_interval - time_total
    if print_overhead: print(f"monitor time: {time_total:.6f}; monitor interval: {monitor_interval:.6f}; sleep_time: {sleep_time:.6f}")
    time.sleep(sleep_time)
    if proc.poll() is not None: break
    time_start = time.time()

    cpu_current = cpu()
    total_diff, idle_diff = (a - b for a, b in zip(cpu_current, cpu_prev))
    cpu_usage.append((1 - idle_diff / total_diff) * 100 if total_diff > 0 else 0)
    cpu_prev = cpu_current

    mem_total, _, mem_avail = mem()
    mem_usage.append((1 - mem_avail / mem_total) * 100)

  stdout, *_ = proc.communicate()
  ptrn = re.compile(r"^\s*(total time:)\s*\b(\d+\.\d+)(h|m|s|ms|us)\b")
  load_time = next(float(p.group(2)) * TIME_UNITS[p.group(3)] for l in stdout.splitlines() if (p := ptrn.search(l.decode())))

  return load_time, cpu_usage, mem_usage, stdout

# example failed sysbench output (invalid total time)
"""
sysbench 0.4.12:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 6

Doing CPU performance benchmark

Threads started!
WARNING: Operation time (18446740473405411328.000000) is greater than maximal counted value, counting as 10000000000000.000000
WARNING: Percentile statistics will be inaccurate
Done.

Maximum prime number checked in CPU test: 100000


Test execution summary:
    total time:                          18446740478.1716s
    total number of events:              10000
    total time taken by event execution: 18446722500.4708
    per-request statistics:
         min:                                  2.03ms
         avg:                            1844672250.05ms
         max:                            18446740473411.55ms
         approx.  95 percentile:               7.80ms

Threads fairness:
    events (avg/stddev):           1666.6667/28.68
    execution time (avg/stddev):   3074453750.0785/15372286728.09
"""

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="A simple argparse example.")
  parser.add_argument("-t", "--threads", type=int, help="number of CPUs to load", required=True)
  parser.add_argument("-p", "--max-prime", type=int, help="maximum prime number passed to sysbench", required=True)
  parser.add_argument("-m", "--monitor-interval", type=float, help="monitor interval in seconds", default=1)
  parser.add_argument("-v", "--verbose", action="count", help="verbose output", default=0)
  args = parser.parse_args()

  load_time, cpu_usage, mem_usage = load(num_threads=args.threads, max_prime=args.max_prime, monitor_interval=args.monitor_interval,
                            print_overhead=args.verbose > 0)
  print(f"load time (s): {load_time}")
  print(f"cpu usage (%): {', '.join(f'{x:.4f}' for x in cpu_usage)}")
  print(f"mem usage (%): {', '.join(f'{x:.4f}' for x in mem_usage)}")
