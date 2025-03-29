#!/usr/bin/env python3

from __future__ import annotations

import os
import time
import monitor
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st
from datetime import datetime
from itertools import zip_longest
from pathlib import Path

OUTDIR = "out"

CI = 0.95
CI_COEFF_THRESHOLD = 0.001
MAX_PRIMES = [ 300000, 500000, 800000, 1200000 ]
TOTAL_CPUS = 12
MONITOR_INTERVAL = 1
# LOAD_MIN_CNT = 30
LOAD_MIN_CNT = 3
LOAD_GROUP_CNT = 3

WIDTH = 100
SEP ="━" * WIDTH

def float_str(f) -> str: return ", ".join(f"{x:.4f}" for x in f)
def np_group_mean(a): return np.array([np.mean([x for x in b if x]) for b in zip_longest(*a)])

def print_info(rt, rt_mean, ci, ci_lower, ci_upper, ci_coeff, prod=None, cpu_group=None, mem_group=None):
    print(SEP)
    print(f"      test count: {len(rt)}")
    print(f"          rt (s): {float_str(rt)}")
    print(f"     mean rt (s): {rt_mean:.4f}")
    print(f"   stddev rt (s): {np.std(rt):.4f}")
    print(f"      {CI*100:3.0f}% ci rt: {ci:.4f} -> [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"     coeff ci rt: {ci_coeff}")
    if prod is not None:
      print(f"            prod: {float_str(prod)}")
      print(f"       mean prod: {np.mean(prod):.4f}")
    if cpu_group is not None:
      print()
      print(f"   usage cpu (%): {float_str(cpu_group)}")
      print(f"    mean cpu (%): {np.mean(cpu_group):.4f}")
    if mem_group is not None:
      print()
      print(f"   usage mem (%): {float_str(mem_group)}")
      print(f"    mean mem (%): {np.mean(mem_group):.4f}")
    print(SEP)

def ci_test():
  resp_times = [8.9911, 8.9986, 8.9716, 8.9801, 8.9869, 8.9809, 9.0023, 8.9838, 8.9808, 8.9785, 8.9852, 8.9705, 8.9768, 8.9871, 8.9779, 9.0564,
                8.9788, 8.9805, 8.9821, 8.9917, 8.9759, 8.9802, 8.996, 8.9817, 8.9939, 9.0299, 9.0303, 9.0397, 9.0384, 9.0468]
  for i in range(2, len(resp_times) + 1, 1):
    rt = np.array(resp_times[:i])
    n = len(rt)
    rt_mean = np.mean(rt)
    ci_lower, ci_upper = st.t.interval(CI, n-1, loc=rt_mean, scale=st.sem(rt))
    ci = ci_upper - rt_mean
    ci_coeff = ci / rt_mean
    print_info(rt, rt_mean, ci, ci_lower, ci_upper, ci_coeff)

def test(threads, max_prime, monitor_interval, load_group_cnt):
  # width = os.get_terminal_size()[0]
  print(SEP)
  print(f"perfoming {load_group_cnt} {max_prime} prime load test with {threads} threads")
  timestamp = datetime.now() # noqa: DTZ005
  dirname = f"{max_prime}-prime-{threads}-threads-{timestamp.strftime('%Y_%m_%d_%H_%M_%S')}"
  title = f"prime={max_prime}; threads={threads}; timestamp={timestamp.strftime('%Y-%m-%d %H:%M:%S')};"

  outdir = Path(f"{OUTDIR}/{dirname}")
  outdir.mkdir(parents=True, exist_ok=True)

  resp_times, cpu_usages, mem_usages = [], [], []
  with (outdir / "sysbench.log").open("w") as f:
    ci_coeff = 1
    i = 0

    while ci_coeff > CI_COEFF_THRESHOLD or i < LOAD_MIN_CNT:
      for _ in range(1, load_group_cnt + 1):
        time.sleep(3)
        load_time, cpu, mem, output = monitor.load(num_threads=threads, max_prime=max_prime, monitor_interval=monitor_interval, print_overhead=False)
        resp_times.append(load_time)
        cpu_usages.append(cpu)
        mem_usages.append(mem)

        load = f"load {(i := i+1)}: {load_time:.4f}s"
        f.write(SEP + "\n")
        f.write(load + "\n")
        f.write(SEP + "\n")
        f.write(output.decode())
        print(load)

      cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
      rt = np.array(resp_times) # type: ignore[assignment]

      n = len(rt)
      prod = np.full(n, max_prime, dtype="float") / rt

      rt_mean = np.mean(rt)
      ci_lower, ci_upper = st.t.interval(CI, n-1, loc=rt_mean, scale=st.sem(rt))
      ci = ci_upper - rt_mean
      ci_coeff = ci / rt_mean
      print_info(rt, rt_mean, ci, ci_lower, ci_upper, ci_coeff, prod, cpu_group, mem_group)

  print(SEP)
  print("FINAL RESULTS")
  print(SEP)
  print("RT")
  print(resp_times)
  print()

  print("CPU")
  print(cpu_usages)
  print()

  print("MEM")
  print(mem_usages)
  print()

  print_info(rt, rt_mean, ci, ci_lower, ci_upper, ci_coeff, prod, cpu_group, mem_group)

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
  # ci_test()
  test(threads=12, max_prime=800000, monitor_interval=1, load_group_cnt=LOAD_GROUP_CNT)

# RESPONSE TIME TESTS @ 9 CPUS (75%)
# 1200000 60s
# 1000000 47s
#  800000 35s
#  600000 24s
#  500000 18s
#  400000 13s
#  300000  9s
#  250000  7s
