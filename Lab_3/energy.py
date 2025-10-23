import glob
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import re

def load_traj(path: Path):
    # wczytaj dane numeryczne
    arr = np.loadtxt(path, comments="#")
    if arr.ndim == 1:
        arr = arr[None, :]
    t = arr[:, 0]
    x = arr[:, 1]
    y = arr[:, 2]

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



files = sorted(glob.glob("Lab_3/traj3_*.txt"))

# for i, fname  in enumerate(files):
#     t, x, y = load_traj(Path(fname))

#     E = 0.5*y**2 + (1 - np.cos(x))
#     dE = E - E[0]

#     plt.plot(t,E)

#     plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.show()


# for i, fname  in enumerate(files):
#     t, x, y, x0, y0 = load_traj(Path(fname))
#     if x0 is not None and y0 is not None:
#         label = f"(x₀={x0:.2f}, y₀={y0:.2f})"

#     E = 0.5*y**2 + (1 - np.cos(x))
#     dE = E - E[0]

#     plt.plot(t, E, label=label)


# plt.legend(loc='best', fontsize=8)
# plt.xlabel("t")
# plt.ylabel("E(t)")
# plt.savefig("delta_E.png")
# plt.show()



t, x, y, x0, y0 = load_traj(Path(files[0]))
E = 0.5*y**2 + (1 - np.cos(x))
dE = E - E[0]

plt.plot(t, dE)
plt.xlabel("t")
plt.ylabel(r"$\Delta E(t)$")
plt.savefig("delta_E_3.png")
plt.show()

