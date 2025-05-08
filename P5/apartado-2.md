---
title: "Práctica Tema 5"
author: "Serafí Nebot Ginard"
date: $DATE$

mainfont: Libertinus Serif
monofont: DejaVu Sans Mono
mathfont: Libertinus Math

documentclass: article
numbersections: true
colorlinks: true
toc: false

geometry: top=2cm, bottom=1.5cm, left=1.5cm, right=1.5cm
pdf-engine: xelatex
header-includes: |
    \usepackage{float}
    \let\origfigure\figure
    \let\endorigfigure\endfigure
    \renewenvironment{figure}[1][H]%
    {\origfigure[H]}{\endorigfigure}

    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \fancyfoot[C]{\thepage}
    \fancyhead[L]{Práctica Tema 5}
    \fancyhead[R]{Serafí Nebot Ginard}
---

# Apartado 2

Implementación del modelo base con el algoritmo MVA en Python3:

```python
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
```

\pagebreak

Resultado de su ejecución:

```
D       D1      D2      Db      N*
0.9400  0.2400  0.7000  0.7000  13.0000

N       R1      R2      R       X0      N1      N2      Rt      Nw      Rz
1       0.0300  0.1000  0.9400  0.1119  0.0268  0.0783  8.9400  0.1051  0.8949
2       0.0308  0.1078  1.0013  0.2222  0.0548  0.1677  9.0013  0.2225  1.7775
3       0.0316  0.1168  1.0705  0.3307  0.0837  0.2703  9.0705  0.3541  2.6459
4       0.0325  0.1270  1.1493  0.4372  0.1137  0.3888  9.1493  0.5025  3.4975
5       0.0334  0.1389  1.2394  0.5412  0.1446  0.5261  9.2394  0.6707  4.3293
6       0.0343  0.1526  1.3430  0.6422  0.1764  0.6860  9.3430  0.8624  5.1376
7       0.0353  0.1686  1.4626  0.7398  0.2089  0.8731  9.4626  1.0819  5.9181
8       0.0363  0.1873  1.6013  0.8332  0.2417  1.0925  9.6013  1.3342  6.6658
9       0.0373  0.2092  1.7628  0.9219  0.2747  1.3503  9.7628  1.6250  7.3750
10      0.0382  0.2350  1.9511  1.0049  0.3074  1.6533  9.9511  1.9607  8.0393
```
