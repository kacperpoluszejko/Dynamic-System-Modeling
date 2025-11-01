import numpy as np
import matplotlib.pyplot as plt
import math


def f(x, y):   # dx/dt
    return y

def g(x, y):   # dy/dt
    return  -2*(y*y/3-1)*y-x
# ===== Siatka =====
x = np.linspace(-3, 3, 70)
y = np.linspace(-3, 3, 70)
X, Y = np.meshgrid(x, y)

U = f(X, Y)
V = g(X, Y)

# Normalizacja (bez NaN w miejscach U=V=0)
N = np.hypot(U, V)
N[N == 0] = 1.0
U_n = U / N
V_n = V / N

fig, ax = plt.subplots(figsize=(7.5, 6.5))

# ===== Portret fazowy =====
#ax.streamplot(X, Y, U, V, density=4, linewidth=0.8, arrowsize=1.0, minlength=0.3)
ax.quiver(X, Y, U_n, V_n,
          angles='xy', scale_units='xy', scale=6,   # spróbuj 20–60
          width=0.002, color='0.5')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.set_aspect('equal', adjustable='box')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', framealpha=0.9)
ax.set_title('Portret fazowy')
plt.tight_layout()
plt.savefig("Fazowy.png")
plt.show()
