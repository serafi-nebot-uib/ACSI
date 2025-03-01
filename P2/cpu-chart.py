#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter

tmsp, pglb, pusr, psys = [], [], [], []
while l := sys.stdin.readline().strip():
  t, g, u, s = l.split(",")
  tmsp.append(t)
  pglb.append(g)
  pusr.append(u)
  psys.append(s)

tmsp = np.array(tmsp, dtype="datetime64")
pglb = np.array(pglb, dtype="float")
pusr = np.array(pusr, dtype="float")
psys = np.array(psys, dtype="float")

fig, ax = plt.subplots()
ax.set_xlabel("timestamp")
ax.set_ylabel("%CPU")
ax.yaxis.set_label_position("left")
ax.yaxis.set_ticks_position("left")
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax.ticklabel_format(style="plain", axis="y")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

ax.plot(tmsp, pglb, linestyle="-", color="r", linewidth=1, label="global")
ax.plot(tmsp, pusr, linestyle="-", color="b", linewidth=1, label="user")
ax.plot(tmsp, psys, linestyle="-", color="g", linewidth=1, label="system")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.legend(loc="upper right")
plt.show()
