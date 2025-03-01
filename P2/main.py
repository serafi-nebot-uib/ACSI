#!/usr/bin/env python3

import sys

while l := sys.stdin.readline().strip():
  tmsp, l = l.split(" %Cpu(s):")
  data = [float(x[:-2]) for x in l.split(",")]
  print(",".join(map(str, (tmsp, 100-data[3], data[0], data[1]))))
