#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter

cols = zip(*(l.strip().split(",") for l in sys.stdin.readlines()))
types = ("datetime64", "float", "uint", "float")
tmsp, cpu, ram, ram_percent = (np.array(d, dtype=dt) for d, dt in zip(cols, types))

# percentage
_, ax_percent = plt.subplots()
ax_percent.set_xlabel("timestamp")
ax_percent.set_ylabel("%")
ax_percent.yaxis.set_label_position("left")
ax_percent.yaxis.set_ticks_position("left")
ax_percent.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax_percent.ticklabel_format(style="plain", axis="y")
ax_percent.set_xticklabels(ax_percent.get_xticklabels(), rotation=90)

ax_percent.plot(tmsp, cpu, linestyle="-", color="b", linewidth=1, label="cpu global")
ax_percent.plot(tmsp, ram_percent, linestyle="-", color="r", linewidth=1, label="ram usage percentage")

plt.legend(loc="upper left")

ax_ram = ax_percent.twinx()
ax_ram.set_xlabel("timestamp")
ax_ram.set_ylabel("bytes")
ax_ram.yaxis.set_label_position("right")
ax_ram.yaxis.set_ticks_position("right")
ax_ram.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax_ram.ticklabel_format(style="plain", axis="y")
ax_ram.set_xticklabels(ax_ram.get_xticklabels(), rotation=90)

ax_ram.plot(tmsp, ram, linestyle="-", color="orange", linewidth=1, label="ram usage")

plt.legend(loc="upper right")

# # 
# _, ax_percent = plt.subplots()
# ax_percent.set_xlabel("timestamp")
# ax_percent.set_ylabel("%")
# ax_percent.yaxis.set_label_position("left")
# ax_percent.yaxis.set_ticks_position("left")
# ax_percent.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
# ax_percent.ticklabel_format(style="plain", axis="y")
# ax_percent.set_xticklabels(ax_ram.get_xticklabels(), rotation=90)
#
# ax_percent.plot(tmsp, used_percent, linestyle="-", color="b", linewidth=1, label="used percent")

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
# plt.legend(loc="upper right")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.show()
