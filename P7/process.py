#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook

def linear_regression(x, y):
  assert x.shape == y.shape, "x and y axis must have the sape shape"
  assert len(x.shape) == 1 == len(x.shape), "input data must only have 1 dimension"
  n = x.shape[0]
  xm, ym = np.mean(x), np.mean(y)
  b = (np.sum(x * y) - n * xm * ym) / (np.sum(x**2) - n * xm**2)
  a = ym - b * xm
  return a, b

def test_linear_regression(x, y):
  a, b = linear_regression(x, y)
  print(a, b)

  fig, ax = plt.subplots(figsize=(12, 8))

  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.scatter(x, y, label="y")

  rx = np.arange(min(x), max(x))
  ry = a + b * rx

  ax.plot(rx, ry, color="red")

  fig.tight_layout()
  plt.show()

wb = load_workbook("data/data.xlsx")
ws = wb.active  # or wb["SheetName"]

rows = ws.iter_rows(values_only=True)
header = next(rows)

req_sec, proc_time, queue_time, send_time = (np.array([b for b in a if b], dtype="float32") for a in zip(*rows))
assert req_sec.size == proc_time.size == queue_time.size == send_time.size, "data sets length mismatch"
total_time = np.array([sum(a) for a in zip(proc_time, queue_time, send_time)])
N = len(total_time)

# x, y = np.arange(0, N), req_sec
x, y = req_sec, proc_time

# N = 100
# np.random.seed(123456789)
# x, y = np.random.randn(N), np.random.randn(N)

test_linear_regression(x, y)
