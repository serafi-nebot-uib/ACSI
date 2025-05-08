#!/usr/bin/env python3

import math

class Service:
  def __init__(self, name, service, visit):
    self.name, self.S, self.V = name, service, visit
    self.D = self.V * self.S
    self.N, self.R, self.X, self.U = ([0.0] for _ in range(4))

cpu, disc = Service("cpu", 0.03, 8.0), Service("disc", 0.1, 7.0)
devs = [cpu, disc]

N, Z = 10, 8.0
V = sum(dev.V for dev in devs)
D = sum(dev.D for dev in devs)
Db = max(dev.D for dev in devs)
Ns = math.ceil((D + Z) / Db)

sep = "\t"
cols = ("D", "D1", "D2", "Db", "N*")
print(sep.join(cols))
data = (D, cpu.D, disc.D, Db, Ns)
print(sep.join(f"{x:.4f}" for x in data), end="\n\n")

X, R, RT, NW, NZ = ([0.0] for _ in range(5))

cols = ("N", "R1", "R2", "R", "X0", "N1", "N2", "Rt", "Nw", "Rz")
print(sep.join(cols))

for n in range(1, N+1):
  R.append(0.0)
  for dev in devs:
    dev.R.append(dev.S * (1 + dev.N[n-1]))
    R[n] += dev.V * dev.R[n]
  RT.append(R[n] + Z)
  X.append(n / (Z + R[n]))
  NW.append(X[n] * R[n])
  NZ.append(X[n] * Z)
  for dev in devs:
    dev.X.append(X[n] * dev.V)
    dev.N.append(dev.X[n] * dev.R[n])
    dev.U.append(dev.X[n] * dev.S)

  Rt = R[n] + Z
  Nw = X[n] * R[n]
  Nz = X[n] * Z
  data = (cpu.R[n], disc.R[n], R[n], X[n], cpu.N[n], disc.N[n], Rt, Nw, Nz)
  print(f"{n}{sep}{sep.join(f"{x:.4f}" for x in data)}")
