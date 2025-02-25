#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
from openpyxl import load_workbook

if __name__ == "__main__":
  assert len(sys.argv) > 1, "incorrect usage"
  workbook = load_workbook(sys.argv[1])

  dates, rt_b, pwr_b = [], [], []
  values = workbook.active.values
  next(values)
  for row in values:
    if row[0] is None: break
    dates.append(row[0])
    rt_b.append(row[2])
    pwr_b.append(row[7])
  dt, rt, pwr = np.array(dates, dtype="datetime64"), np.array(rt_b), np.array(pwr_b)
  e = rt * pwr


  fig, ax_rt = plt.subplots()
  ax_rt.set_xlabel("timestamp")
  ax_pwr = ax_rt.twinx()

  ax_rt.plot(dt, rt, linestyle="-", color="b", linewidth=1)
  ax_rt.set_ylabel("second (s)")
  ax_pwr.plot(dt, e, linestyle="-", color="r", linewidth=1)
  ax_pwr.set_ylabel("watt second (Ws)")

  # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

  plt.show()
