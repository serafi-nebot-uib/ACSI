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

def ma(y, n):
  assert len(x.shape) == 1, "input data must only have 1 dimension"
  return np.array([np.mean(y[i-n:i]) for i in range(n, len(y))])

def exp(y, alpha):
  assert len(x.shape) == 1, "input data must only have 1 dimension"
  assert 0 < alpha < 1, "alpha must be 0 < alpha < 1"
  ft = np.ones_like(y)
  ft[0] = y[0]
  for i in range(1, x.shape[0]): ft[i] = ft[i-1] + alpha * (y[i] - ft[i-1])
  return ft

wb = load_workbook("data/data.xlsx")
ws = wb.active  # or wb["SheetName"]

rows = ws.iter_rows(values_only=True)
header = next(rows)

req_sec, proc_time, queue_time, send_time = (np.array([b for b in a if b], dtype="float32") for a in zip(*rows))
assert req_sec.size == proc_time.size == queue_time.size == send_time.size, "data sets length mismatch"
total_time = np.array([sum(a) for a in zip(proc_time, queue_time, send_time)])
N = len(total_time)

x, y = np.arange(0, N), req_sec
# x, y = req_sec, proc_time

a, b = linear_regression(x, y)
print(f"linear regression: a + b * x = {a:.4f} + {b:.4f} * x")

ma70, ma500, ma2000 = ma(y, 70), ma(y, 500), ma(y, 2000)

ey = exp(y, alpha=0.6)

fig, ax = plt.subplots(figsize=(12, 8))

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.scatter(x, y, label="y")
# ax.plot(x, y, label="y")

rx = np.arange(min(x), max(x))
ry = a + b * rx

ax.plot(x, ey, color="blue", label="exp")
ax.plot(x[70:], ma70, color="orange", label="MA 70")
ax.plot(x[500:], ma500, color="green", label="MA 500")
ax.plot(x[2000:], ma2000, color="magenta", label="MA 2000")
ax.plot(rx, ry, color="red", label="linear regression")

fig.tight_layout()
plt.legend()
plt.show()
