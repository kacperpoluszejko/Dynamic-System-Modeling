#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import glob, re, os, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--dir", default=".", help="katalog z plikami traj_m_*_x0_*.txt (domyślnie bieżący)")
args = parser.parse_args()

base = args.dir
pattern = os.path.join(base, "**", "traj_m_*_x0_*.txt")
files = sorted(glob.glob(pattern, recursive=True))
if not files:
    print(f"Nie znaleziono plików dla wzorca: {pattern}", file=sys.stderr)
    sys.exit(1)

pat = re.compile(r"traj_m_([+-]?\d+(?:\.\d+)?)_x0_([+-]?\d+(?:\.\d+)?)\.txt$", re.IGNORECASE)

by_m = defaultdict(list)
for f in files:
    name = os.path.basename(f)
    m0 = pat.search(name)
    if not m0:
        continue
    m = float(m0.group(1))
    x0 = float(m0.group(2))
    by_m[m].append((x0, f))

if not by_m:
    print("Znaleziono pliki, ale żaden nie pasuje do wzorca nazwy.", file=sys.stderr)
    sys.exit(1)

for m in sorted(by_m.keys()):
    curves = sorted(by_m[m], key=lambda t: t[0])
    plt.figure(figsize=(8,5))
    any_curve = False
    for x0, fname in curves:
        try:
            data = np.loadtxt(fname, comments="#")
        except Exception as e:
            print(f"Problem z wczytaniem {fname}: {e}", file=sys.stderr)
            continue
        if data.ndim == 1 or data.shape[1] < 2:
            continue
        t, x = data[:,0], data[:,1]
        plt.plot(t, x, lw=0.9, label=f"x0={x0:+.1f}")
        any_curve = True

    if not any_curve:
        plt.close()
        print(f"Brak danych do narysowania dla m={m:+.3f}", file=sys.stderr)
        continue

    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.ylim(-5, 5)
    plt.title(f"Rozwiązania dla p = {m:+.3f}")
    plt.grid(True, alpha=0.4)
    # plt.legend(ncol=3, fontsize=7)
    plt.tight_layout()
    outname = f"traj_plot_m_{m:+.3f}.png"
    plt.savefig(outname, dpi=200)
    plt.show()
    plt.close()
    print(f"Zapisano wykres: {outname}")
