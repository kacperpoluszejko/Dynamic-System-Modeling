#!/usr/bin/env python3
import glob
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import re

# ===== definicja układu =====
def f(x, y):   # dx/dt
    return x * (y - 1.0)

def g(x, y):   # dy/dt
    return 3.0*x - 2.0*y + x**2 - 2.0*y**2

# ===== funkcja do wczytania trajektorii i warunków początkowych =====
def load_traj(path: Path):
    # wczytaj dane numeryczne
    arr = np.loadtxt(path, comments="#")
    if arr.ndim == 1:
        arr = arr[None, :]
    t = arr[:, 0]
    x = arr[:, 1]
    y = arr[:, 2]

    # spróbuj wyciągnąć x0, y0 z nagłówka
    x0 = y0 = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") and "x0" in line and "y0" in line:
                m = re.search(r"x0\s*=\s*([-\d.eE]+)", line)
                n = re.search(r"y0\s*=\s*([-\d.eE]+)", line)
                if m and n:
                    x0 = float(m.group(1))
                    y0 = float(n.group(1))
                break

    return t, x, y, x0, y0


def main():
    files = sorted(glob.glob("Lab_2/traj_*.txt"))
    if not files:
        print("Brak plików traj_*.txt")
        return

    # ===== Portret fazowy =====
    all_x, all_y, all_x0y0 = [], [], []
    for fname in files:
        t, x, y, x0, y0 = load_traj(Path(fname))
        all_x.append(x)
        all_y.append(y)
        all_x0y0.append((x0, y0))

    xmin, xmax = -4, 3
    ymin, ymax = -4, 3

    fig, ax = plt.subplots(figsize=(8, 7))

    # Pole wektorowe
    nx = ny = 25
    X, Y = np.meshgrid(np.linspace(xmin, xmax, nx),
                       np.linspace(ymin, ymax, ny))
    U = f(X, Y)
    V = g(X, Y)
    N = np.hypot(U, V)
    N[N == 0] = 1.0
    ax.quiver(X, Y, U/N, V/N, angles='xy', scale_units='xy', scale=5,
              width=0.003, color='0.75', pivot='mid')

    # Izokliny
    ax.axvline(0, color='tab:blue', linestyle='--', lw=1.3, label='f=0')
    ax.axhline(1, color='tab:blue', linestyle='--', lw=1.3)
    xx = np.linspace(xmin-0.5, xmax+0.5, 1200)
    disc = 1 + 2*xx**2 + 6*xx
    mask = disc >= 0
    yy_plus  = (-1 + np.sqrt(disc[mask])) / 2
    yy_minus = (-1 - np.sqrt(disc[mask])) / 2
    ax.plot(xx[mask], yy_plus,  color='tab:red', linestyle='--', lw=1.3, label='g=0')
    ax.plot(xx[mask], yy_minus, color='tab:red', linestyle='--', lw=1.3)

    # Trajektorie z podpisem punktu początkowego
    for fname, x, y, (x0, y0) in zip(files, all_x, all_y, all_x0y0):
        if x0 is not None and y0 is not None:
            label = f"(x₀={x0:.2f}, y₀={y0:.2f})"
        else:
            label = f"{Path(fname).name}"
        ax.plot(x, y, lw=1.8, label=label)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=8)
    ax.set_title('Portret fazowy z trajektoriami (punkty początkowe w legendzie)')
    plt.tight_layout()
    plt.savefig("portret_fazowy.png")
    plt.show()

    # ===== Wykresy x(t), y(t) =====
    for i, fname  in enumerate(files):
        t, x, y, x0, y0 = load_traj(Path(fname))
        fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 6), sharex=True)
        if x0 is not None and y0 is not None:
            fig2.suptitle(f"(x₀={x0:.2f}, y₀={y0:.2f})")
        else:
            fig2.suptitle(Path(fname).name)

        ax1.plot(t, x, lw=1.8, color='tab:blue')
        ax1.set_ylabel('x(t)')
        ax1.grid(True, alpha=0.3)

        ax2.plot(t, y, lw=1.8, color='tab:orange')
        ax2.set_xlabel('t')
        ax2.set_ylabel('y(t)')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f"traj_{i:02d}_xt_yt.png")
    plt.show()


if __name__ == "__main__":
    main()
