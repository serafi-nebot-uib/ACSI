#!/usr/bin/env python3

from __future__ import annotations

import os
import monitor
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats as st
from itertools import zip_longest
from pathlib import Path

CI = 0.95
OUTDIR = "out"

def float_str(f) -> str: return ", ".join(f"{x:.4f}" for x in f)
def np_group_mean(a): return np.array([np.mean([x for x in b if x]) for b in zip_longest(*a)])

def test(threads, max_prime, monitor_interval, load_group_cnt): # noqa: PLR0915
  # width = os.get_terminal_size()[0]
  width = 100
  sep ="━" * width
  print(sep)
  print(f"perfoming {load_group_cnt} {max_prime} prime load test with {threads} threads")
  timestamp = datetime.now() # noqa: DTZ005
  dirname = f"{max_prime}-prime-{threads}-threads-{timestamp.strftime('%Y_%m_%d_%H_%M_%S')}"
  title = f"prime={max_prime}; threads={threads}; timestamp={timestamp.strftime('%Y-%m-%d %H:%M:%S')};"

  outdir = Path(f"{OUTDIR}/{dirname}")
  outdir.mkdir(parents=True, exist_ok=True)

  resp_times, cpu_usages, mem_usages = [], [], []
  with (outdir / "sysbench.log").open("w") as f:
    for i in range(1, load_group_cnt + 1):
      load_time, cpu, mem, output = monitor.load(num_threads=threads, max_prime=max_prime, monitor_interval=monitor_interval, print_overhead=False)
      resp_times.append(load_time)
      cpu_usages.append(cpu)
      mem_usages.append(mem)

      load = f"load {i}: {load_time:.4f}s"
      f.write(sep + "\n")
      f.write(load + "\n")
      f.write(sep + "\n")
      f.write(output.decode())
      print(load)

  cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
  resp_times = np.array(resp_times) # type: ignore[assignment]

  n = len(resp_times)
  prod = np.full(n, max_prime, dtype="float") / resp_times

  mean = np.mean(resp_times)
  ci_lower, ci_upper = st.t.interval(CI, n-1, loc=mean, scale=st.sem(resp_times))
  valid = [x for x in resp_times if ci_lower <= x <= ci_upper]
  valid_percent = len(valid) / len(resp_times) * 100

  print(f"          rt (s): {float_str(resp_times)}")
  print(f"     mean rt (s): {mean:.4f}")
  print(f"   stddev rt (s): {np.std(resp_times):.4f}")
  print(f"      {CI*100:3.0f}% ci rt: {ci_lower:.4f} {ci_upper:.4f}")
  print(f"            prod: {float_str(prod)}")
  print(f"       mean prod: {np.mean(prod):.4f}")
  print(f"           valid: {float_str(valid)}")
  print(f"         valid %: {valid_percent:.4f}")
  print()
  print(f"   usage cpu (%): {float_str(cpu_group)}")
  print(f"    mean cpu (%): {np.mean(cpu_group):.4f}")
  print(f"   usage mem (%): {float_str(mem_group)}")
  print(f"    mean mem (%): {np.mean(mem_group):.4f}")

  # fig_rt, ax_rt = plt.subplots(figsize=(16, 9))
  # ax_rt.set_ylabel("seconds")
  # ax_rt.yaxis.set_label_position("left")
  # ax_rt.yaxis.set_ticks_position("left")
  # ax_rt.bar(labels, resp_times)
  # fig_rt.legend(loc="upper right")
  # fig_rt.suptitle(f"Response Time [{title}]", fontsize=16, fontweight="bold")
  # fig_rt.savefig(str(outdir / "response-time.png"))

  # fig_cpu, ax_cpu = plt.subplots(figsize=(16, 9))
  # ax_cpu.boxplot(cpu_usages)

  # fig_usage, ax_usage_percent = plt.subplots(figsize=(16, 9))
  # ax_usage_percent.set_ylabel("%")
  # ax_usage_percent.yaxis.set_label_position("left")
  # ax_usage_percent.yaxis.set_ticks_position("left")
  # x = np.arange(0, len(cpu_group), monitor_interval)
  # print(len(x), x)
  # print(len(cpu_usages), cpu_usages)
  # ax_usage_percent.set_xticks(x)
  #
  # ax_usage_percent.plot(x, cpu_group, color="blue", linestyle="-", linewidth=1, label="CPU usage (%)")
  # ax_usage_percent.plot(x, mem_group, color="red", linestyle="-", linewidth=1, label="MEM usage (%)")
  #
  # fig_usage.legend(loc="upper right")
  # fig_usage.suptitle(f"CPU & MEM usage [{title}]", fontsize=16, fontweight="bold")
  # fig_usage.savefig(str(outdir / "usage.png"))

  # plt.show()

if __name__ == "__main__":
  MAX_PRIMES = [ 150000, 300000, 500000, 600000 ]
  THREADS = 6
  MONITOR_INTERVAL = 1
  LOAD_GROUP_CNT = 3

  # test(THREADS, MAX_PRIME, MONITOR_INTERVAL, 3)
  test(threads=6, max_prime=150000, monitor_interval=1, load_group_cnt=1)

"""
RESPONSE TIME TESTS [6 THREADS (75% CPU)]
  150000 8s
  300000 20s
  500000 40s
  600000 52s
  800000 78s
  1000000 100s

CHOSEN BENCHMARKS
  150000 300000 500000 600000
"""

"""
MONITOR TIME TESTS
     monitor time: 0.000281, 0.000135, 0.000171, 0.000579, 0.000216, 0.000200, 0.000258, 0.000227, 0.000221, 0.000196, 0.000162, 0.000180, 0.000189, 0.000185, 0.000193, 0.000185, 0.000317, 0.000221
mean monitor time: 0.000229
overhead: Tm / Ti = 0.000229 / 1.0 = 0.000229 -> 0.0229 %
"""
