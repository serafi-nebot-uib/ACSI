#!/usr/bin/env python3

import re
import time
import subprocess
from pathlib import Path

TIME_UNITS = { "h": 60*60, "m": 60, "s": 1, "ms": 1/1000, "us": 1/1000000 }

def cpu_usage():
  with Path("/proc/stat").open("r") as f:
    # cpu [user] [nice] [system] [idle] [iowait] [irq] [softirq] [steal] [guest] [guest_nice]
    fields = list(map(int, f.readline().strip().split()[1:]))
    user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice = fields
    idle_time = idle + iowait
    total_time = user + nice + system + idle_time + irq + softirq + steal + guest + guest_nice
    return total_time, idle_time

def cpu_load(*, num_threads: int = 6, max_prime: int = 100000, monitor_interval: int = 1, print_overhead: int = False):
  prev, time_start = cpu_usage(), time.time()

  load_cmd = ["sysbench", f"--num-threads={num_threads}", "--test=cpu", f"--cpu-max-prime={max_prime}", "run"]
  load = subprocess.Popen(load_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa: S603

  cpu = []
  while True:
    time_total = time.time() - time_start
    sleep_time = monitor_interval - time_total
    if print_overhead: print(f"monitor time: {time_total:.6f}; monitor interval: {monitor_interval:.6f}; sleep_time: {sleep_time:.6f}")
    time.sleep(sleep_time)
    if load.poll() is not None: break
    time_start = time.time()
    current = cpu_usage()
    total_diff, idle_diff = (a - b for a, b in zip(current, prev))
    cpu.append((1 - idle_diff / total_diff) * 100 if total_diff > 0 else 0)
    prev = current

  stdout, _ = load.communicate()
  ptrn = re.compile(r"^\s*(total time:)\s*\b(\d+\.\d+)(h|m|s|ms|us)\b")
  total_time = next(float(p.group(2)) * TIME_UNITS[p.group(3)] for l in stdout.splitlines() if (p := ptrn.search(l.decode())))
  return total_time, cpu

total_time, cpu = cpu_load(num_threads=6, max_prime=100000)
print(f"cpu usage: {cpu}")
print(f"total time: {total_time}")
