#!/usr/bin/env python3
import re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def parse_y0_from_header(path: Path):
    y0 = None
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                break
            m = re.search(r'y0\s*=\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)', line)
            if m:
                try:
                    y0 = float(m.group(1))
                except ValueError:
                    pass
    return y0

def load_data(path: Path):
    arr = np.loadtxt(path, comments='#')
    if arr.ndim == 1:
        arr = arr[None, :]
    t, y_num, y_exact = arr[:, 0], arr[:, 1], arr[:, 2]
    return t, y_num, y_exact

def main():
    files = sorted(Path('.').glob('Lab_2/wynik_*.txt'))
    if not files:
        print("Brak plików wynik_*.txt")
        return

    for f in files:
        t, y_num, y_exact = load_data(f)
        y0 = parse_y0_from_header(f)

        plt.figure()
        plt.plot(t, y_num, label='y_num')
        plt.plot(t, y_exact, linestyle='--', label='y_exact')
        title = f.name if y0 is None else f"{f.name}  (y0={y0})"
        plt.title(title)
        plt.xlabel('t')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"Wykres {f.name}.png")

    plt.show()

if __name__ == "__main__":
    main()
