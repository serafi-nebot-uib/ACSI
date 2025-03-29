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

def chart():
  pass

def test(threads, max_prime, monitor_interval, load_group_cnt):
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

  # resp_times, cpu_usages, mem_usages = [], [], []
  # with (outdir / "sysbench.log").open("w") as f:
  #   for i in range(1, load_group_cnt + 1):
  #     load_time, cpu, mem, output = monitor.load(num_threads=threads, max_prime=max_prime, monitor_interval=monitor_interval, print_overhead=False)
  #     resp_times.append(load_time)
  #     cpu_usages.append(cpu)
  #     mem_usages.append(mem)
  #
  #     load = f"load {i}: {load_time:.4f}s"
  #     f.write(sep + "\n")
  #     f.write(load + "\n")
  #     f.write(sep + "\n")
  #     f.write(output.decode())
  #     print(load)

  resp_times = [8.9706, 8.9722, 8.9607, 9.0913, 8.9782, 8.9616, 9.0925, 8.9766, 8.9610, 8.9648, 8.9705, 8.9676, 8.9624, 8.9593, 8.9796, 8.9574, 9.0534, 9.0130, 8.9835, 8.9623, 8.9624, 8.9534, 9.0169, 9.0017, 8.9653, 8.9591, 8.9810, 8.9553, 8.9771, 9.0853]
  cpu_usages = [[75.4671, 75.3470, 75.0541, 75.0923, 75.0477, 75.0291, 75.0701, 75.0576, 75.0208]] * 30
  mem_usages = [[13.5310, 13.5309, 13.5307, 13.5308, 13.5307, 13.5304, 13.5303, 13.5299, 13.5272]] * 30

  cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
  resp_times = np.array(resp_times) # type: ignore[assignment]

  n = len(resp_times)
  prod = np.full(n, max_prime, dtype="float") / resp_times

  mean = np.mean(resp_times)
  ci_lower, ci_upper = st.t.interval(CI, n-1, loc=mean, scale=st.sem(resp_times))
  ci = ci_upper - mean

  print(f"          rt (s): {float_str(resp_times)}")
  print(f"     mean rt (s): {mean:.4f}")
  print(f"   stddev rt (s): {np.std(resp_times):.4f}")
  print(f"      {CI*100:3.0f}% ci rt: {ci:.4f} -> [{ci_lower:.4f}, {ci_upper:.4f}]")
  print(f"     coeff ci rt: {ci / mean}")
  print(f"            prod: {float_str(prod)}")
  print(f"       mean prod: {np.mean(prod):.4f}")
  print()
  print(f"   usage cpu (%): {float_str(cpu_group)}")
  print(f"    mean cpu (%): {np.mean(cpu_group):.4f}")
  print(f"   usage mem (%): {float_str(mem_group)}")
  print(f"    mean mem (%): {np.mean(mem_group):.4f}")
  print()
  print()

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
  MAX_PRIMES = [ 300000, 500000, 800000, 1200000 ]
  THREADS = 6
  MONITOR_INTERVAL = 1
  LOAD_GROUP_CNT = 3
  CI_COEFF_THRESHOLD = 0.02

  test(threads=9, max_prime=300000, monitor_interval=1, load_group_cnt=3*10)

# RESPONSE TIME TESTS @ 9 CPUS (75%)
# 1200000 60s
# 1000000 47s
#  800000 35s
#  600000 24s
#  500000 18s
#  400000 13s
#  300000  9s
#  250000  7s
