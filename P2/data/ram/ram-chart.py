#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter

cols = zip(*(l.strip().split(",") for l in sys.stdin.readlines()))
types = ("datetime64", "uint", "uint", "float")
tmsp, free, used, used_percent = (np.array(d, dtype=dt) for d, dt in zip(cols, types))

print(f"free mean: {np.mean(free)} KB")
print(f"used mean: {np.mean(used)} KB")

# RAM KB
fig_ram, ax_ram = plt.subplots()
ax_ram.set_xlabel("timestamp")
ax_ram.set_ylabel("KB")
ax_ram.yaxis.set_label_position("left")
ax_ram.yaxis.set_ticks_position("left")
ax_ram.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax_ram.ticklabel_format(style="plain", axis="y")
ax_ram.set_xticklabels(ax_ram.get_xticklabels(), rotation=90)

ax_ram.plot(tmsp, free, linestyle="-", color="g", linewidth=1, label="free")
ax_ram.plot(tmsp, used, linestyle="-", color="r", linewidth=1, label="used")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.legend(loc="upper right")

# RAM %
fig_percent, ax_percent = plt.subplots()
ax_percent.set_xlabel("timestamp")
ax_percent.set_ylabel("%")
ax_percent.yaxis.set_label_position("left")
ax_percent.yaxis.set_ticks_position("left")
ax_percent.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax_percent.ticklabel_format(style="plain", axis="y")
ax_percent.set_xticklabels(ax_ram.get_xticklabels(), rotation=90)

ax_percent.plot(tmsp, used_percent, linestyle="-", color="b", linewidth=1, label="used percent")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.legend(loc="upper right")
plt.show()
