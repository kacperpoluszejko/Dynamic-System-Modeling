import numpy as np
import matplotlib.pyplot as plt

# ========= Układ =========
# x' = y
# y' = -2*((y**2)/3 - 1)*y - x
def f(x, y):   # dx/dt
    return y

def g(x, y):   # dy/dt
    return -2*((y*y)/3 - 1)*y - x

# ========= Siatka =========
x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)

U = f(X, Y)
V = g(X, Y)
speed = np.hypot(U, V)  # wielkość wektora pola (do koloru i grubości)

# ========= Rysunek =========
fig, ax = plt.subplots(figsize=(8, 7))

# Strumienie z kolorem wg prędkości i zmienną grubością linii
lw = 0.5 + 2.0 * (speed / (speed.max() if speed.max() != 0 else 1.0))  # grubość
strm = ax.streamplot(
    X, Y, U, V,
    density=1.2,          # gęstość linii (1.0–2.0)
    linewidth=lw,         # zmienna grubość
    color=speed,          # kolor wg prędkości
    cmap='viridis',       # mapa kolorów (np. 'plasma', 'magma', 'turbo')
    arrowsize=1.3,        # rozmiar grotów
    minlength=0.2,
)

# # ========= Nullkliny =========
# # \dot x = 0  => y = 0
# ax.axhline(0, linestyle='--', linewidth=1.2, alpha=0.8, color='tab:orange', label=r'$\dot x=0$')

# # \dot y = 0  => x = -2*((y^2)/3 - 1)*y
# yy = np.linspace(-3, 3, 800)
# xx = -2*((yy**2)/3 - 1)*yy
# ax.plot(xx, yy, linestyle='--', linewidth=1.2, alpha=0.8, color='tab:blue', label=r'$\dot y=0$')

# # ========= Punkt równowagi =========
# ax.plot(0, 0, 'o', color='tab:cyan', label='punkt równowagi')

# ========= Oś, siatka, tytuł =========
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal', adjustable='box')
ax.grid(True, alpha=0.25)
# ax.set_title(r'Portret fazowy: $\dot x = y$, $\dot y = -2\left(\frac{y^2}{3}-1\right)y - x$')

# ========= Kolorbar =========
# cbar = fig.colorbar(strm.lines, ax=ax, pad=0.02)
# cbar.set_label(r'$\sqrt{(\dot x)^2+(\dot y)^2}$')

# ========= Legenda i zapis =========
ax.legend(loc='upper left', framealpha=0.9)
plt.tight_layout()
plt.savefig("phase_portrait_improved.png", dpi=200, bbox_inches='tight')
plt.show()
