#!/usr/bin/env python3

from tinygrad import Tensor, dtypes
from tinygrad.helpers import Timing

with Timing("euclidian distance calculation (upper triangular matrix): "):
  xt = [19.3, 14.4, 12.5, 8.6, 6, 4, 2]
  yt = [21.9, 19, 15, 7.6, 5.2, 3.6, 2.7]
  N = len(xt)
  x = Tensor(xt, dtype=dtypes.float32)
  y = Tensor(yt, dtype=dtypes.float32)

  diff_x = (x.unsqueeze(0) - x.unsqueeze(1)).triu()
  diff_y = (y.unsqueeze(0) - y.unsqueeze(1)).triu()
  dist = (diff_x**2 + diff_y**2).sqrt()

  m = dist.numpy()
  print(m)
  mval = m[m != 0].min()

  mcoords = ((i, j) for i in range(N-1) for j in range(i+1, N) if abs(m[i][j] - mval) < 0.001)
  for i, j in mcoords: print(f"m[{i}][{j}]: {m[i][j]}")

