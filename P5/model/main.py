#!/usr/bin/env python3

class Service:
  def __init__(self, name, service, visit):
    self.name, self.S, self.V = name, service, visit
    self.N = [0.0]
    self.R = [0.0]
    self.X = [0.0]
    self.U = [0.0]

  def __repr__(self): return f"Service({self.name}, service={self.S})"

cpu = Service("cpu", 0.03, 8.0)
disc = Service("disc", 0.1, 7.0)
devs = [cpu, disc]

N = 10
X = [0.0]
Z = 8.0
V = sum(dev.V for dev in devs)
R = [0.0]
RT = [0.0]
NW = [0.0]
NZ = [0.0]
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

sep = "\t"
cols = ("N", "R1", "R2", "R", "X0", "N1", "N2", "Rt", "Nw", "Rz")
print(sep.join(cols))
for n, data in enumerate(zip(cpu.R, disc.R, R, X, cpu.N, disc.N, RT, NW, NZ)):
  if n == 0: continue
  s = sep.join(f"{x:.4f}" for x in data)
  print(f"{n}{sep}{s}")
