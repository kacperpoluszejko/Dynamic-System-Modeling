#!/usr/bin/env python3
import glob
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import re


# ===== funkcja do wczytania trajektorii i warunków początkowych =====
def load_traj(path: Path):
    arr = np.loadtxt(path, comments="#")
    if arr.ndim == 1:
        arr = arr[None, :]
    t = arr[:, 0]
    x = arr[:, 1]
    v = arr[:, 2]

    x0 = v0 = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") and "x0" in line and "z0" in line:
                m = re.search(r"x0\s*=\s*([-\d.eE]+)", line)
                n = re.search(r"z0\s*=\s*([-\d.eE]+)", line)
                if m and n:
                    x0 = float(m.group(1))
                    v0 = float(n.group(1))
                break

    return t, x, v, x0, v0


def main():

    # ======= wczytujemy wszystkie pliki z trajektorami =======
    files = sorted(glob.glob("Lab_6/traj_m_*.txt"))
    if not files:
        print("Brak plików traj_m_*.txt!")
        return

    # ======= grupujemy pliki według wartości m =======
    m_groups = {}   # słownik: m → lista plików

    for f in files:
        name = Path(f).name
        match = re.search(r"traj_m_([0-9.]+)_run(\d+)\.txt", name)
        if not match:
            print("Pomijam plik niepasujący:", name)
            continue

        m_val = float(match.group(1))

        if m_val not in m_groups:
            m_groups[m_val] = []
        m_groups[m_val].append(f)

    # ======= iterujemy po wszystkich wartościach m =======
    for m_val, flist in m_groups.items():
        print(f"\n=== Rysuję wykresy dla m = {m_val:.6f} ===")

        # ===== PORTRET FAZOWY =====
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.set_title(f"Trajektorie w przestrzeni fazowej (m = {m_val:.6f})")

        for fname in flist:
            t, x, v, x0, v0 = load_traj(Path(fname))

            if x0 is not None and v0 is not None:
                label = f"(x₀={x0:.3f}, v₀={v0:.3f})"
            else:
                label = Path(fname).name

            ax.plot(x, v, lw=1.4, label=label)

        ax.set_xlabel("x")
        ax.set_ylabel("v")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        plt.tight_layout()
        plt.savefig(f"portret_fazowy_m_{m_val:.6f}.png")

        # ===== WYKRESY x(t), v(t) =====
        for i, fname in enumerate(flist):
            t, x, v, x0, v0 = load_traj(Path(fname))

            fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 6), sharex=True)

            if x0 is not None and v0 is not None:
                fig2.suptitle(f"(x₀={x0:.3f}, v₀={v0:.3f}), m={m_val:.6f}")
            else:
                fig2.suptitle(f"{Path(fname).name}")

            ax1.plot(t, x, lw=1.8)
            ax1.set_ylabel("x(t)")
            ax1.grid(True, alpha=0.3)

            ax2.plot(t, v, lw=1.8)
            ax2.set_ylabel("v(t)")
            ax2.set_xlabel("t")
            ax2.grid(True, alpha=0.3)

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig(f"traj_xt_vt_m_{m_val:.6f}_run{i+1}.png")


if __name__ == "__main__":
    main()
