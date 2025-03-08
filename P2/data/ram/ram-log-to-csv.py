#!/usr/bin/env python3

import sys

import random
from datetime import datetime

# cat /proc/meminfo | head -n 1
RAM_TOTAL = 12227312

# vmstat 3 3601 --unit K --wide
tmsp = 1740825604.0
while l := sys.stdin.readline().strip():
  if l[0] == "-":
    next(sys.stdin)
    continue
  free = int(l.split()[3])
  used = RAM_TOTAL - free
  used_percent = used / RAM_TOTAL * 100
  t = datetime.fromtimestamp(tmsp).strftime("%Y-%m-%d %H:%M:%S")
  print(",".join(map(str, (t, free, used, used_percent))))
  tmsp += 3 + random.uniform(0, 100) / 10000
