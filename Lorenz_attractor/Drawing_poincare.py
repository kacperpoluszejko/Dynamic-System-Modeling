import numpy as np
import matplotlib.pyplot as plt
from glob import glob

z0 = 0.0  # wartość z definiująca płaszczyznę przekroju Poincarégo: z = z0, z0 = rho - 1

xs_all = []
ys_all = []

# Wczytanie trajektorii dla danego rho (tu: rho = 1.00) i wszystkich warunków początkowych
for fname in sorted(glob("Lorenz_attractor/lorenz_rho_001.00_ic_*.txt")):
    data = np.loadtxt(fname)

    # Kolumny: t, x, y, z
    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]

    # Wykrycie przecięć z płaszczyzną z=z0 poprzez zmianę znaku (z - z0) między kolejnymi krokami
    mask = (z[:-1] - z0) * (z[1:] - z0) < 0

    # Interpolacja liniowa punktu przecięcia (dokładniejsze niż branie najbliższej próbki)
    alpha = (z0 - z[:-1][mask]) / (z[1:][mask] - z[:-1][mask])

    # Wyznaczenie współrzędnych (x,y) w punktach przecięcia z płaszczyzną przekroju
    xs = x[:-1][mask] + alpha * (x[1:][mask] - x[:-1][mask])
    ys = y[:-1][mask] + alpha * (y[1:][mask] - y[:-1][mask])

    xs_all.append(xs)
    ys_all.append(ys)

# Połączenie punktów przecięć ze wszystkich trajektorii (różne warunki początkowe)
xs_all = np.concatenate(xs_all)
ys_all = np.concatenate(ys_all)

# Wykres przekroju Poincarégo w przestrzeni (x,y)
plt.scatter(xs_all, ys_all, s=0.1)
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.savefig("Poincare_z0_5.png")
plt.show()
