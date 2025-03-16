#!/usr/bin/env python3

import monitor
import numpy as np
import matplotlib.pyplot as plt
from itertools import zip_longest

THREADS, MAX_PRIME, MONITOR_INTERVAL = 6, 100000, 1

def confidence_interval(data, confidence_level=0.95):
  data = np.asarray(data)
  if confidence_level not in [0.90, 0.95, 0.99]: raise ValueError("Only confidence levels 0.90, 0.95, 0.99 are supported")
  z_scores = { 0.90: 1.645, 0.95: 1.96, 0.99: 2.576 }
  z = z_scores[confidence_level]
  n, mean, std = len(data), np.mean(data), np.std(data, ddof=1)  # ddof=1 for sample standard deviation
  if n < 2: return (np.nan, np.nan)
  me = z * std / np.sqrt(n)
  return (mean - me, mean + me)

_, ax = plt.subplots()
ax.set_xlabel("time (s)")
ax.set_ylabel("cpu usage (%)")
ax.yaxis.set_label_position("left")
ax.yaxis.set_ticks_position("left")
# ax.set_ylim(0, 100)

# times, usages = [], []
# for i in range(3):
#   load_time, usage = monitor.load(num_threads=THREADS, max_prime=MAX_PRIME, monitor_interval=MONITOR_INTERVAL, print_overhead=False)
#   times.append(load_time)
#   usages.append(usage)
#   print(f"test {i}: {load_time:.6f}s")
#
#   x, y = np.arange(0, len(usage), MONITOR_INTERVAL), np.array(usage, dtype="float64")
#   ax.plot(x, y, linestyle="-", linewidth=1, label=f"load {i}")
#
# print(times)
# print(usages)
#
# plt.legend(loc="upper right")
# plt.show()

# SIMULATE

times = [4.6204, 4.6959, 5.1367]
usages = [
  [75.25, 75.31172069825436, 75.03121098626717, 75.125],
  [75.625, 75.25, 75.0, 75.03121098626717],
  [74.81296758104739, 75.37688442211055, 75.03121098626717, 74.9685534591195, 75.03121098626717]
]

# take the mean of each time period
group = [np.mean(np.array(list(filter(None, a)))) for a in zip_longest(*usages)]
std = np.std(group)
ci = confidence_interval(group, confidence_level=0.95)
print(f"group: {group}")
print(f"mean: {np.mean(group):.4f}; std: {std:.4f}; ci: {ci}")
