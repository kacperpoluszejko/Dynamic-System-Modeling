import numpy as np
import matplotlib.pyplot as plt
from glob import glob

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for fname in sorted(glob("Lorenz_attractor/traj3_*.txt")):
    data = np.loadtxt(fname)
    x = data[:,1]
    y = data[:,2]
    z = data[:,3]
    ax.plot(x, y, z, linewidth=0.8)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()

for fname in sorted(glob("Lorenz_attractor/traj3_*.txt")):
    data = np.loadtxt(fname)
    x = data[:,1]
    z = data[:,3]
    plt.plot(x, z, linewidth=0.8)

plt.xlabel("x")
plt.ylabel("z")
plt.axis("equal")
plt.show()


d1 = np.loadtxt("Lorenz_attractor/traj3_01.txt")
d2 = np.loadtxt("Lorenz_attractor/traj3_02.txt")

plt.plot(d1[:,0], d1[:,1], label="IC 1")
plt.plot(d2[:,0], d2[:,1], label="IC 2")

plt.xlabel("t")
plt.ylabel("x(t)")
plt.legend()
plt.show()