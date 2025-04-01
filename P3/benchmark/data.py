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
CPU_TOTAL = 12

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

def rt_prod_chart(labels, max_primes, resp_times, xlabel=None):
  assert len(labels) == len(max_primes) == len(resp_times)

  plot_rt, plot_prod = [], []
  for prime, rt_list in zip(max_primes, resp_times):
    rt = np.array(rt_list)
    rt_mean = np.mean(rt)
    prod = np.full(len(rt_list), prime, dtype="float") / rt
    prod_mean = np.mean(prod)
    plot_rt.append(float(rt_mean))
    plot_prod.append(float(prod_mean))

  positions = np.arange(len(labels))
  width = 0.35

  fig_rt, ax_rt = plt.subplots(figsize=(12, 9))

  print(f"primes: {max_primes}")
  print(f"    rt: {plot_rt}")
  print(f"  prod: {plot_prod}")

  ax_rt.set_xticks(positions)
  ax_rt.set_xticklabels(labels)
  if isinstance(xlabel, str): ax_rt.set_xlabel(xlabel)
  ax_prod = ax_rt.twinx()

  ax_rt.bar(positions - width/2, plot_rt, width=width, color="blue", label="tiempo respuesta (segundos)")
  ax_prod.bar(positions + width/2, plot_prod, width=width, color="orange", label="productividad (primos/segundo)")

  ax_rt.yaxis.set_label_position("left")
  ax_rt.yaxis.set_ticks_position("left")
  ax_rt.set_ylabel("segundos")

  ax_prod.yaxis.set_label_position("right")
  ax_prod.yaxis.set_ticks_position("right")
  ax_prod.set_ylabel("primos/segundo")

  fig_rt.legend(loc="upper right")
  fig_rt.suptitle("Tiempo de respuesta y productividad", fontsize=16, fontweight="bold")

  plt.show()

def cpu_mem_prime_chart(max_primes, cpu_usages, mem_usages):
  assert len(max_primes) == len(cpu_usages) == len(mem_usages)

  plot_labels, plot_cpu, plot_mem = [], [], []
  for prime, cpu, mem in zip(max_primes, cpu_usages, mem_usages):
    cpu_mean, mem_mean = np.mean(np_group_mean(cpu)), np.mean(np_group_mean(mem))
    plot_cpu.append(cpu_mean)
    plot_mem.append(mem_mean)
    plot_labels.append(str(prime))

  print(plot_labels)
  print(plot_cpu)
  print(plot_mem)

  positions = np.arange(len(plot_labels))
  width = 0.35

  fig_cpu_mem, ax_cpu = plt.subplots(figsize=(12, 9))

  ax_cpu.set_xticks(positions)
  ax_cpu.set_xticklabels(plot_labels)
  ax_cpu.set_xlabel("max prime")
  ax_mem = ax_cpu.twinx()

  ax_cpu.bar(positions - width/2, plot_cpu, width=width, color="blue", label="% CPU")
  ax_mem.bar(positions + width/2, plot_mem, width=width, color="red", label="% MEM")

  ax_cpu.yaxis.set_label_position("left")
  ax_cpu.yaxis.set_ticks_position("left")
  ax_cpu.set_ylabel("% CPU")

  ax_mem.yaxis.set_label_position("right")
  ax_mem.yaxis.set_ticks_position("right")
  ax_mem.set_ylabel("% MEM")

  fig_cpu_mem.legend(loc="upper right")
  fig_cpu_mem.suptitle("CPU & MEM usage", fontsize=16, fontweight="bold")

  plt.show()

def cpu_mem_chart(prime, rt_list, cpu_usages, mem_usages):
  assert len(rt_list) == len(cpu_usages) == len(mem_usages)

  fig_cpu, ax_cpu = plt.subplots(figsize=(16, 9))
  ax_cpu.set_xlabel("execution time (s)")
  ax_cpu.yaxis.set_label_position("left")
  ax_cpu.yaxis.set_ticks_position("left")
  ax_cpu.set_ylabel("cpu usage (%)")

  fig_mem, ax_mem = plt.subplots(figsize=(16, 9))
  ax_mem.set_xlabel("execution time (s)")
  ax_mem.yaxis.set_label_position("left")
  ax_mem.yaxis.set_ticks_position("left")
  ax_mem.set_ylabel("mem usage (%)")

  for i, rt, cpu, mem in zip(range(n), rt_list, cpu_usages, mem_usages):
    ax_cpu.plot(range(len(cpu)), cpu, label=f"load {i+1} ({rt}s)")
    ax_mem.plot(range(len(mem)), mem, label=f"load {i+1} ({rt}s)")

  cpu_mean, mem_mean = np_group_mean(cpu_usages), np_group_mean(mem_usages)
  ax_cpu.plot(range(len(cpu_mean)), cpu_mean, linestyle="--", label="cpu mean")
  ax_mem.plot(range(len(mem_mean)), mem_mean, linestyle="--", label="mem mean")

  fig_cpu.legend(loc="upper right")
  fig_cpu.suptitle(f"CPU usage [{prime} max prime]", fontsize=16, fontweight="bold")
  fig_mem.legend(loc="upper right")
  fig_mem.suptitle(f"MEM usage [{prime} max prime]", fontsize=16, fontweight="bold")

  plt.show()

def phase_1():
  data_dir = Path("data/phase_1")
  tests = [ (300000, 9), (500000, 9), (800000, 9), (1200000, 9), (800000, 12) ]

  rt_list, cpu_usages, mem_usages = [], [], []
  for max_prime, threads in tests:
    with (data_dir / f"{max_prime}-{threads}.csv").open("r") as f:
      reader = csv.reader(f)
      next(reader)
      resp_times = [float(x) for x in next(reader)]
      n = len(resp_times)
      rt_list.append(resp_times)

      next(reader)
      next(reader)
      cpu_usages.append([[float(x) for x in next(reader)] for _ in range(n)])

      next(reader)
      next(reader)
      mem_usages.append([[float(x) for x in next(reader)] for _ in range(n)])

  def part_1():
    idx = [i for i in range(len(tests)) if tests[i][1] == 9]
    max_primes = [tests[i][0] for i in idx]
    rt = [rt_list[i] for i in idx]
    cpu = [cpu_usages[i] for i in idx]
    mem = [mem_usages[i] for i in idx]
    rt_prod_chart(max_primes, max_primes, rt, xlabel="carga (max prime)")
    # cpu_mem_prime_chart(max_primes, cpu, mem)
    # for prime, r, c, m in zip(max_primes, rt, cpu, mem): cpu_mem_chart(prime, r, c, m)

  def part_2():
    idx = [i for i in range(len(tests)) if tests[i][0] == 800000]
    labels = [f"{tests[i][1] / CPU_TOTAL * 100:.0f}%" for i in idx]
    max_primes = [tests[i][0] for i in idx]
    rt = [rt_list[i] for i in idx]
    rt_prod_chart(labels, max_primes, rt, xlabel="utilización CPU")

  # part_1()
  part_2()

def phase_2():
  data_dir = Path("data/phase_2")
  tests = [ (800000, 3), (800000, 6), (800000, 9), (800000, 12) ]

  rt_list, prod_list, cpu_usages, mem_usages = [], [], [], []
  for max_prime, threads in tests:
    with (data_dir / f"{max_prime}-{threads}.csv").open("r") as f:
      reader = csv.reader(f)
      next(reader)
      resp_times = [float(x) for x in next(reader)]
      n = len(resp_times)
      rt_list.append(resp_times)
      prod_list.append(800000 / np.mean(resp_times))

      next(reader)
      next(reader)
      cpu_usages.append([[float(x) for x in next(reader)] for _ in range(n)])

      next(reader)
      next(reader)
      mem_usages.append([[float(x) for x in next(reader)] for _ in range(n)])

  cpu_cnt = [x[1] for x in tests]
  cpu_percent = [x[1] / CPU_TOTAL for x in tests]
  labels = [f"{x[1] / CPU_TOTAL * 100:.0f}%" for x in tests]
  rt = rt_list
  cpu = cpu_usages
  mem = mem_usages
  # rt_prod_chart(labels, [800000] * len(rt), rt, xlabel="utilización CPU")

  rt_25, rt_50, rt_75, rt_100 = [np.mean(x) for x in rt]

  print("  25 / 25: ",  rt_25 / rt_25)
  print("  25 / 50: ",  rt_25 / rt_50)
  print("  25 / 75: ",  rt_25 / rt_75)
  print(" 25 / 100: ", rt_25 / rt_100)

  print("  50 / 25: ",  rt_50 / rt_25)
  print("  50 / 50: ",  rt_50 / rt_50)
  print("  50 / 75: ",  rt_50 / rt_75)
  print(" 50 / 100: ", rt_50 / rt_100)

  print("  75 / 25: ",  rt_75 / rt_25)
  print("  75 / 50: ",  rt_75 / rt_50)
  print("  75 / 75: ",  rt_75 / rt_75)
  print(" 75 / 100: ", rt_75 / rt_100)

  print(" 100 / 25: ",  rt_100 / rt_25)
  print(" 100 / 50: ",  rt_100 / rt_50)
  print(" 100 / 75: ",  rt_100 / rt_75)
  print("100 / 100: ", rt_100 / rt_100)

  print()

  print("rt/cpu")
  print(f" 25%:  {rt_25 / cpu_cnt[0]}")
  print(f" 50%:  {rt_50 / cpu_cnt[1]}")
  print(f" 75%:  {rt_75 / cpu_cnt[2]}")
  print(f"100%: {rt_100 / cpu_cnt[3]}")

  print()

  print("rt*cpu")
  print(f" 25%:  {rt_25 * cpu_percent[0]}")
  print(f" 50%:  {rt_50 * cpu_percent[1]}")
  print(f" 75%:  {rt_75 * cpu_percent[2]}")
  print(f"100%: {rt_100 * cpu_percent[3]}")

  # print()
  #
  # prod_25, prod_50, prod_75, prod_100 = prod_list
  # print("prod/cpu")
  # print(f" 25%: {prod_25 / cpu_cnt[0]}")
  # print(f" 50%: {prod_50 / cpu_cnt[1]}")
  # print(f" 75%: {prod_75 / cpu_cnt[2]}")
  # print(f"100%: {prod_100 / cpu_cnt[3]}")

if __name__ == "__main__":
  # phase_1()
  phase_2()
