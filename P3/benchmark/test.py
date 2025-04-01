#!/usr/bin/env python3

from __future__ import annotations

import time
import monitor
import numpy as np
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
LOAD_MIN_CNT = 250
# LOAD_MIN_CNT = 3
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
  resp_times = [8.9784, 8.981, 8.9903, 8.9757, 8.9538, 8.942, 8.9582, 8.9766, 8.9948, 8.9872, 9.0245, 8.9752, 8.9796, 8.9806, 8.9912, 8.9809, 8.981, 8.9752, 8.9837, 8.979, 8.9787, 8.9811, 8.9872, 8.983, 9.0059, 9.0011, 8.9888, 8.9767, 8.9721, 8.9777, 8.9778, 8.9807, 8.9841, 8.9797, 9.0261, 8.9769, 8.9843, 8.9757, 8.9719, 8.9798, 8.979, 8.9859, 9.0004, 8.9959, 8.9848, 8.989, 8.9984, 8.9974, 8.9726, 8.9874, 8.9762, 8.98, 8.9801, 8.9831, 8.9829, 8.9809, 8.9867, 8.9793, 9.0029, 8.9789, 8.9753, 8.9792, 8.9946, 9.0023, 8.9694, 8.9709, 8.9816, 8.9929, 8.9931, 8.9804, 8.9956, 8.9836, 8.9713, 8.9769, 8.9713, 8.9691, 8.9771, 8.9955, 8.9725, 8.9734, 8.9806, 8.9803, 9.0173, 8.9814, 8.9902, 9.0444, 9.0387, 9.0503, 9.0446, 9.0572, 9.0455, 9.0489, 9.0542, 9.0441, 9.0505, 9.04, 9.0437, 9.0401, 9.0624, 9.0635, 9.0681, 9.0803, 9.0487, 9.04, 9.0465, 9.0509, 9.0434, 9.0542, 9.0489, 9.0269, 9.0583, 9.0472, 9.0467, 9.0443, 9.0466, 9.0473, 9.0404, 9.0528, 9.0501, 9.0475, 9.0268, 9.0511, 9.0502, 9.0718, 9.0531, 9.0468, 9.0437, 9.0479, 9.0473, 9.0429, 9.049, 9.0487, 9.07, 9.0383, 9.0469, 9.0527, 9.0641, 9.0418, 9.0552, 9.0476, 9.064, 9.0601, 9.0546, 9.0507, 9.0289, 9.0342, 9.0382, 9.0462, 9.0546, 9.0403, 9.0361, 9.0526, 9.0442, 9.0464, 9.0482, 9.0327, 9.0476, 9.0436, 9.0429, 9.0457, 9.0622, 9.0449, 9.05, 9.0337, 9.0464, 9.0393, 9.0622, 9.0578, 9.0549, 9.0508, 9.0414, 9.0473, 9.0476, 9.0573, 9.0424, 9.0476, 9.0507, 9.0591, 9.0409, 9.0423, 9.0312, 9.0385, 9.0527, 9.0498, 9.0664, 9.0763, 9.0458, 9.0421, 9.0501, 9.0574, 9.0445, 9.074, 9.0425, 9.0557, 9.0554, 9.0447, 9.0369, 9.0432, 9.0645, 9.0557, 9.0554, 9.0435, 9.0458, 9.0357, 9.0409, 9.0471, 9.0337, 9.0238, 9.0524, 9.0368, 9.0312, 9.0538, 9.0554, 9.0404, 9.0445, 9.0286, 9.0429, 9.0552, 9.0416, 9.0418, 9.0381, 9.0495, 9.04, 9.0475, 9.0553, 9.0317, 9.0501, 9.0406, 9.039, 9.0434, 9.049, 9.0777, 9.0485, 9.0409, 9.0392, 9.05, 9.0286, 9.0449, 9.0498, 9.0386, 9.0332, 9.0518, 9.0572, 9.0493, 9.0456, 9.0625, 9.0379, 9.0414, 9.1098, 9.0603, 9.0494, 9.0418]
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

if __name__ == "__main__":
  ci_test()
  # test(threads=int(12 * 0.75), max_prime=300000, monitor_interval=1, load_group_cnt=LOAD_GROUP_CNT)

# RESPONSE TIME TESTS @ 9 CPUS (75%)
# 1200000 60s
# 1000000 47s
#  800000 35s
#  600000 24s
#  500000 18s
#  400000 13s
#  300000  9s
#  250000  7s
