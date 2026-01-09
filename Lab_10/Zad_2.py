import numpy as np
import matplotlib.pyplot as plt

r = 3.569945672
N = 200000
burn = 2000

x_old = 0.5
x_list = []

for i in range(N):
    x_new = r * x_old * (1 - x_old)
    if i >= burn:
        x_list.append(x_new)
    x_old = x_new

x = np.array(x_list)
x = (x - x.min()) / (x.max() - x.min())



#eps_list = [2e-2, 1e-2, 5e-3, 5e-4]
eps_list = [5e-4]

for eps in eps_list:
    n_bins = int(1.0 / eps)
    counts, edges = np.histogram(x, bins=n_bins, range=(0, 1))
    centers = 0.5 * (edges[:-1] + edges[1:])
    plt.step(centers, counts, where="mid", label=f"ε={eps:g}")

    plt.xlim(0.225, 0.325)
    plt.yscale("log")
    plt.xlabel("x")
    plt.ylabel("liczba punktów w przedziale")
    plt.legend()
    plt.tight_layout()
    plt.savefig("hist_3.png")
    plt.show()