import numpy as np
import matplotlib.pyplot as plt
from glob import glob

z0 = 27.0

xs_all = []
ys_all = []

for fname in sorted(glob("Lorenz_attractor/lorenz_rho_028.00_ic_*.txt")):
    data = np.loadtxt(fname)

    x = data[:,1]
    y = data[:,2]
    z = data[:,3]

    mask = (z[:-1] - z0) * (z[1:] - z0) < 0

    alpha = (z0 - z[:-1][mask]) / (z[1:][mask] - z[:-1][mask])

    xs = x[:-1][mask] + alpha * (x[1:][mask] - x[:-1][mask])
    ys = y[:-1][mask] + alpha * (y[1:][mask] - y[:-1][mask])

    xs_all.append(xs)
    ys_all.append(ys)

xs_all = np.concatenate(xs_all)
ys_all = np.concatenate(ys_all)

plt.scatter(xs_all, ys_all, s=0.1)
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.savefig("Poincare_z0.png")
plt.show()
