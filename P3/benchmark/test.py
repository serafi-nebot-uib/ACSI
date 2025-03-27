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

MIN_TESTS, CI = 5, 0.95
OUTDIR = "out"

def float_str(f) -> str: return ", ".join(f"{x:.4f}" for x in f)
def np_group_mean(a): return np.array([np.mean([x for x in b if x]) for b in zip_longest(*a)])

def test(threads, max_prime, monitor_interval):
  # width = os.get_terminal_size()[0]
  width = 100
  sep ="━" * width
  print(sep)
  print(f"perfoming {max_prime} prime load test with {threads} threads")
  timestamp = datetime.now() # noqa: DTZ005
  name = f"{max_prime}-prime-{threads}-threads-{timestamp.strftime('%Y_%m_%d_%H_%M_%S')}"

  Path(OUTDIR).mkdir(parents=True, exist_ok=True)

  with Path(f"{OUTDIR}/{name}.log").open("w") as f:
    times, cpu_usages, mem_usages = [], [], []
    for i in range(MIN_TESTS):
      load_time, cpu, mem, output = monitor.load(num_threads=threads, max_prime=max_prime, monitor_interval=monitor_interval, print_overhead=False)
      times.append(load_time)
      cpu_usages.append(cpu)
      mem_usages.append(mem)

      load = f"load {i}: {load_time:.4f}s"
      f.write(sep + "\n")
      f.write(load + "\n")
      f.write(sep + "\n")
      f.write(output.decode())
      print(load)

  cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
  times = np.array(times) # type: ignore[assignment]

  n = len(times)
  prod = np.full(n, MAX_PRIME, dtype="float") / times

  mean = np.mean(times)
  ci_lower, ci_upper = st.t.interval(CI, n-1, loc=mean, scale=st.sem(times))

  def ci_check(val): return ci_lower <= val <= ci_upper

  print(f"   usage cpu (%): {float_str(cpu_group)}")
  print(f"    mean cpu (%): {np.mean(cpu_group):.4f}")
  print(f"   usage mem (%): {float_str(mem_group)}")
  print(f"    mean mem (%): {np.mean(mem_group):.4f}")
  print(f"       times (s): {float_str(times)}")
  print(f" me an times (s): {mean:.4f}")
  print(f"stddev times (s): {np.std(times):.4f}")
  print(f"   {CI*100:3.0f}% ci times: {ci_lower:.4f} {ci_upper:.4f}")
  print(f"            prod: {float_str(prod)}")
  print(f"       mean prod: {np.mean(prod):.4f}")

  valid = [x for x in times if ci_check(x)]
  valid_percent = len(valid) / len(times) * 100
  print()
  print(f"           valid: {float_str(valid)}")
  print(f"         valid %: {valid_percent:.4f}")

  fig, ax_time = plt.subplots(figsize=(16, 9))
  ax_time.set_ylabel("seconds")
  ax_time.yaxis.set_label_position("left")
  ax_time.yaxis.set_ticks_position("left")
  ax_time.plot(np.arange(0, len(times), MONITOR_INTERVAL), times, color="red", linestyle="-", linewidth=1, label="response time (s)")
  ax_time.axhspan(ci_lower, ci_upper, color="red", alpha=0.15, label="95% CI range")

  # ax_prod = ax_time.twinx()
  # ax_prod.set_ylabel("productivity")
  # ax_prod.yaxis.set_label_position("right")
  # ax_prod.yaxis.set_ticks_position("right")
  # ax_prod.plot(np.arange(0, len(times), MONITOR_INTERVAL), prod, color="green", linestyle="-", linewidth=1, label="productivity")

  fig.suptitle(name)
  fig.savefig(f"{OUTDIR}/{name}.png")
  # plt.show()

if __name__ == "__main__":
  THREADS, MAX_PRIME, MONITOR_INTERVAL = 6, 50000, 1
  test(THREADS, MAX_PRIME, MONITOR_INTERVAL)
# # SIMULATE
# # times = [5.0109, 4.7901, 4.7693]
# # cpu_usages = [[75.31172069825436, 75.15605493133583, 75.0, 75.03121098626717, 75.03121098626717], [75.43640897755611, 75.125, 75.125, 75.093399750934], [74.84355444305382, 75.81047381546135, 75.03121098626717, 75.125]]
# # mem_usages = [[14.906465133138013, 14.906465133138013, 14.906465133138013, 14.906465133138013, 14.906465133138013], [14.906465133138013, 14.906465133138013, 14.906465133138013, 14.906465133138013], [14.906465133138013, 14.906465133138013, 14.906465133138013, 14.906465133138013]]
#
# # 150000 10
# # times = [8.0604, 8.1006, 8.2513, 8.126, 8.1932, 8.1037, 8.1241, 8.1171, 8.2839, 8.1395]
# # cpu_usages = [[75.25, 75.18703241895261, 75.09386733416771, 75.12437810945273, 75.03121098626717, 75.03121098626717, 75.21793275217932, 74.90636704119851], [75.43640897755611, 75.18703241895261, 75.21793275217932, 75.09386733416771, 75.03121098626717, 75.34246575342466, 75.06265664160401, 75.06234413965088], [75.375, 75.18703241895261, 75.18703241895261, 75.21902377972467, 75.125, 75.093399750934, 75.125, 75.06234413965088], [75.15605493133583, 75.18703241895261, 75.125, 75.03121098626717, 75.03121098626717, 75.15605493133583, 75.125, 75.09386733416771], [75.21902377972467, 75.25, 75.06234413965088, 75.15605493133583, 75.03121098626717, 75.09386733416771, 75.093399750934, 75.5], [75.03121098626717, 75.18703241895261, 75.09386733416771, 75.093399750934, 75.06265664160401, 74.93765586034912, 75.0, 75.06234413965088], [75.06234413965088, 75.25, 75.125, 75.125, 75.03121098626717, 75.093399750934, 75.15605493133583, 75.0], [75.15605493133583, 75.37313432835822, 75.06234413965088, 75.093399750934, 75.15605493133583, 75.06234413965088, 75.09386733416771, 75.093399750934], [75.71964956195244, 75.49751243781094, 75.125, 75.06234413965088, 75.125, 75.0, 75.15605493133583, 75.15527950310559], [76.0, 75.40574282147317, 75.18703241895261, 75.03121098626717, 75.125, 75.0, 75.18703241895261, 75.15605493133583]]
# # mem_usages = [[15.049096645280668, 15.049096645280668, 15.049096645280668, 15.049096645280668, 15.049096645280668, 15.049096645280668, 15.049096645280668, 15.049096645280668], [15.049096645280668, 15.049096645280668, 15.050928609656811, 15.050928609656811, 15.050928609656811, 15.038072145374226, 15.038333854570817, 15.038333854570817], [15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817], [15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817], [15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817, 15.038333854570817], [15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974], [15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974], [15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974], [15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974], [15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974, 15.040394814493974]]
#
# # 50000 20
#   times = [1.8783, 1.8865, 1.8982, 1.8926, 1.8963, 1.8911, 1.895, 1.8897, 1.9018, 1.883, 1.8885, 1.8938, 1.8935, 1.8906, 1.8946, 1.8907, 1.8958, 1.8925, 1.8913, 1.8937]
#   cpu_usages = [[75.03121098626717], [75.46699875466999], [75.31172069825436], [75.31172069825436], [75.40574282147317], [75.24875621890547], [75.75], [75.43640897755611], [75.06234413965088], [75.40574282147317], [75.2808988764045], [75.15605493133583], [75.40574282147317], [75.21793275217932], [75.15605493133583], [75.65217391304347], [75.46699875466999], [75.37313432835822], [75.40574282147317], [75.31172069825436]]
#   mem_usages = [[15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.02410341700613], [15.026164376929286], [15.026164376929286], [15.026164376929286], [15.026164376929286], [15.026164376929286], [15.026164376929286], [15.028225336852453], [15.026164376929286], [15.026164376929286], [15.028225336852453], [15.026164376929286]]
#
# # times, cpu_usages, mem_usages = [], [], []
# # for i in range(MIN_TESTS):
# #   load_time, cpu, mem, output = monitor.load(num_threads=THREADS, max_prime=MAX_PRIME, monitor_interval=MONITOR_INTERVAL, print_overhead=False)
# #   times.append(load_time)
# #   cpu_usages.append(cpu)
# #   mem_usages.append(mem)
# #   print(f"load {i}: {load_time:.4f}s")
#
#   print(times)
#   print(cpu_usages)
#   print(mem_usages)
#
# # take the mean of each time period
#   cpu_group, mem_group = np_group_mean(cpu_usages), np_group_mean(mem_usages)
#   times = np.array(times) # type: ignore[assignment]
#
#   n = len(times)
#   prod = np.full(n, MAX_PRIME, dtype="float") / times
#
#   mean = np.mean(times)
#   ci_lower, ci_upper = st.t.interval(CI, n-1, loc=mean, scale=st.sem(times))
#
#   def ci_check(val): return ci_lower <= val <= ci_upper
#
#   print(f"   usage cpu (%): {float_str(cpu_group)}")
#   print(f"    mean cpu (%): {np.mean(cpu_group):.4f}")
#   print(f"   usage mem (%): {float_str(mem_group)}")
#   print(f"    mean mem (%): {np.mean(mem_group):.4f}")
#   print(f"       times (s): {float_str(times)}")
#   print(f" me an times (s): {mean:.4f}")
#   print(f"stddev times (s): {np.std(times):.4f}")
#   print(f"   {CI*100:3.0f}% ci times: {ci_lower:.4f} {ci_upper:.4f}")
#   print(f"            prod: {float_str(prod)}")
#   print(f"       mean prod: {np.mean(prod):.4f}")
#
#   valid = [x for x in times if ci_check(x)]
#   valid_percent = len(valid) / len(times) * 100
#   print()
#   print(f"           valid: {float_str(valid)}")
#   print(f"         valid %: {valid_percent:.4f}")
#
#   _, ax_time = plt.subplots(figsize=(16, 9))
#   ax_time.set_ylabel("seconds")
#   ax_time.yaxis.set_label_position("left")
#   ax_time.yaxis.set_ticks_position("left")
#
#   x = np.arange(0, len(times), MONITOR_INTERVAL)
#
#   ax_time.plot(x, times, color="red", linestyle="-", linewidth=1, label="response time (s)")
#   ax_time.axhspan(ci_lower, ci_upper, color="red", alpha=0.15, label="95% CI range")
# # plt.errorbar(x=range(n), y=times, yerr=me, fmt="o", label="95% CI")
# # plt.axhline(float(mean), linestyle="--", label="Mean")
#   plt.legend(loc="upper left")
#
# # ax_prod = ax_time.twinx()
# # ax_prod.set_ylabel("productivity")
# # ax_prod.yaxis.set_label_position("right")
# # ax_prod.yaxis.set_ticks_position("right")
# #
# # ax_prod.plot(x, prod, color="green", linestyle="-", linewidth=1, label="productivity")
#
#   plt.legend(loc="upper right")
#   plt.show()
