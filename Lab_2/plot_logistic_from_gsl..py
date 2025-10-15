# plot_logistic_from_gsl.py
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

HEADER_RE = re.compile(r"#\s*x0\s*=\s*([+-]?\d+(?:\.\d*)?)")

def load_blocks(fname):
    """Wczytuje plik w formacie:
       # x0=...
       t   x
       ...
       (pusta linia)   -> następny blok
       Zwraca listę krotek: (x0, t_array, x_array)
    """
    blocks = []
    x0 = None
    t_list, y_list = [], []

    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                # koniec bloku
                if x0 is not None and t_list:
                    blocks.append((x0, np.array(t_list), np.array(y_list)))
                x0 = None
                t_list, y_list = [], []
                continue

            if line.startswith("#"):
                m = HEADER_RE.search(line)
                if m:
                    x0 = float(m.group(1))
                continue

            # dane
            parts = line.split()
            if len(parts) >= 2:
                t_list.append(float(parts[0]))
                y_list.append(float(parts[1]))

    # ostatni blok (gdy plik nie kończy się pustą linią)
    if x0 is not None and t_list:
        blocks.append((x0, np.array(t_list), np.array(y_list)))

    return blocks

def plot_blocks(blocks, title, outfile):
    plt.figure()
    # posortuj po x0, żeby legenda była ładna
    blocks_sorted = sorted(blocks, key=lambda b: b[0])
    for x0, t, x in blocks_sorted:
        plt.plot(t, x, label=f"x0={x0:.1f}")
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.title(title)
    plt.grid(True, which="both", ls=":")
    # przy wielu krzywych legenda poza wykresem bywa czytelniejsza:
    plt.legend(ncol=2, fontsize=8, loc="upper left", bbox_to_anchor=(1.02, 1.0))
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.show()

def main():
    f1 = Path("traj_k1.txt")
    f2 = Path("traj_k-1.txt")
    if not f1.exists() or not f2.exists():
        raise SystemExit("Brakuje plików traj_k1.txt / traj_k-1.txt w bieżącym katalogu.")

    blocks_k1  = load_blocks(f1)
    blocks_km1 = load_blocks(f2)

    plot_blocks(blocks_k1,  "x' = +1 * x(1-x)", "plot_k1.png")
    plot_blocks(blocks_km1, "x' = -1 * x(1-x)", "plot_k-1.png")

if __name__ == "__main__":
    main()
