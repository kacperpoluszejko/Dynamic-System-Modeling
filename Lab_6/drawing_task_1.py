#!/usr/bin/env python3
import glob
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import re


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
    files = sorted(glob.glob("Lab_6/trajm3_*.txt"))
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

    xmin, xmax = -10, 10
    ymin, ymax = -10, 10

    fig, ax = plt.subplots(figsize=(8, 7))


    # Trajektorie z podpisem punktu początkowego
    for fname, x, y, (x0, y0) in zip(files, all_x, all_y, all_x0y0):
        if x0 is not None and y0 is not None:
            label = f"(x₀={x0:.4f}, v₀={y0:.2f})"
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
    ax.set_title('Trajektorie w przestrzeni fazowej (m = 3)')
    plt.tight_layout()
    plt.savefig("portret_fazowy_z_trajektoriami22_m_3.png")
    plt.show()

    # ===== Wykresy x(t), y(t) =====
    for i, fname  in enumerate(files):
        t, x, y, x0, y0 = load_traj(Path(fname))
        fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 6), sharex=True)
        if x0 is not None and y0 is not None:
            fig2.suptitle(f"(x₀={x0:.4f}, v₀={y0:.2f})")
        else:
            fig2.suptitle(Path(fname).name)

        ax1.plot(t, x, lw=1.8, color='tab:blue')
        ax1.set_ylabel('x(t)')
        ax1.grid(True, alpha=0.3)

        ax2.plot(t, y, lw=1.8, color='tab:orange')
        ax2.set_xlabel('t')
        ax2.set_ylabel('v(t)')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f"traj22_{i:02d}_xt_yt_m_3.png")
    plt.show()


if __name__ == "__main__":
    main()
