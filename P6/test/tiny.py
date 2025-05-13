#!/usr/bin/env python3

from tinygrad import Tensor, dtypes
from tinygrad.helpers import Timing
from openpyxl import load_workbook

with Timing("data load: "):
  wb = load_workbook("data.xlsx")
  ws = wb.active  # or wb["SheetName"]

  rows = ws.iter_rows(values_only=True)
  header = next(rows)

  req_sec, proc_time, queue_time, send_time = ([b for b in a if b] for a in zip(*rows))
  assert len(req_sec) == len(proc_time) == len(queue_time) == len(send_time), "data sets length mismatch"
  total_time = [sum(a) for a in zip(proc_time, queue_time, send_time)]
  N = len(total_time)

with Timing("euclidian distance calculation (upper triangular matrix): "):
  x = Tensor(req_sec[:N], dtype=dtypes.float32)
  y = Tensor(total_time[:N], dtype=dtypes.float32)

  diff_x = x.unsqueeze(0) - x.unsqueeze(1)
  diff_y = y.unsqueeze(0) - y.unsqueeze(1)
  dist = (diff_x**2 + diff_y**2).sqrt()

  # dist.min().numpy()

  mask = Tensor.eye(*dist.shape, fill_value=float("inf"))
  # inf = Tensor.full(shape=dist.shape, fill_value=float("inf")).tril(diagonal=0)
  res = dist + mask
  print(mask.numpy())
  print(res.numpy())
  # print(res.min().numpy())

  # m = dist.numpy()
  # print(m)
  # mval = m[m != 0].min()
  # print(mval)

  # mcoords = ((i, j) for i in range(N-1) for j in range(i+1, N) if abs(m[i][j] - mval) == 0)
  # for i, j in mcoords: print(f"m[{i}][{j}]: {m[i][j]}")
