#!/usr/bin/env python3

from __future__ import annotations

import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from itertools import zip_longest


CI = 0.95
WIDTH = 100
SEP = "━" * WIDTH

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

if __name__ == "__main__":
  tests = [ (300000, 9), (500000, 9), (800000, 9), (1200000, 9) ]

  plot_rt = []
  plot_prod = []
  plot_labels = []

  data_dir = Path("data")
  for max_prime, threads in tests:
    with (data_dir / f"{max_prime}-{threads}.csv").open("r") as f:
      reader = csv.reader(f)
      next(reader)
      resp_times = [float(x) for x in next(reader)]
      n = len(resp_times)

      next(reader)
      next(reader)
      cpu_usages = [[float(x) for x in next(reader)] for _ in range(n)]

      next(reader)
      next(reader)
      mem_usages = [[float(x) for x in next(reader)] for _ in range(n)]

      cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
      rt = np.array(resp_times)
      rt_mean = np.mean(rt)
      prod = np.full(n, max_prime, dtype="float") / rt
      prod_mean = np.mean(prod)

      plot_rt.append(float(rt_mean))
      plot_prod.append(float(prod_mean))
      plot_labels.append(str(max_prime)) # convert to string to avoid invisible bars (or specify bar width)

  print(plot_prod)

  positions = np.arange(len(plot_labels))
  width = 0.35

  fig_rt, ax_rt = plt.subplots(figsize=(12, 9))

  ax_rt.set_xticks(positions)
  ax_rt.set_xticklabels(plot_labels)
  ax_rt.set_xlabel("max prime")
  ax_prod = ax_rt.twinx()

  ax_rt.bar(positions - width/2, plot_rt, width=width, color="blue", label="response time (second)")
  ax_prod.bar(positions + width/2, plot_prod, width=width, color="orange", label="productivity (prime/second)")

  ax_rt.yaxis.set_label_position("left")
  ax_rt.yaxis.set_ticks_position("left")
  ax_rt.set_ylabel("seconds")

  ax_prod.yaxis.set_label_position("right")
  ax_prod.yaxis.set_ticks_position("right")
  ax_prod.set_ylabel("prime/second")

  fig_rt.legend(loc="upper right")
  fig_rt.suptitle("Response Time and Production", fontsize=16, fontweight="bold")
  plt.show()
