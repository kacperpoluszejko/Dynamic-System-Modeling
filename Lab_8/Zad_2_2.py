import numpy as np
import matplotlib.pyplot as plt
import os

K_table = np.array([0.5, 0.971635, 5.0])
os.makedirs("poincare_zad_2", exist_ok=True)

b = 0.001
N = 2000

theta0 = np.pi
alpha = np.arange(0, 1, 0.02)
L0_list = alpha * 2*np.pi

for K in K_table:
    points_theta = []
    points_L = []

    for L0 in L0_list:
        theta = theta0
        L = L0

        for _ in range(N):
            points_theta.append(theta % (2*np.pi))
            points_L.append(L)

            L_old = L
            theta_old = theta

            L = (L_old + K*np.sin(theta_old)) * np.exp(-b)
            theta = theta_old + (L_old + K*np.sin(theta_old)) * ((1 - np.exp(-b)) / b)

    plt.figure(figsize=(6,6))
    plt.scatter(points_theta, points_L, s=1)
    plt.xlabel(r"$\theta \;(\mathrm{mod}\; 2\pi)$")
    plt.ylabel(r"$L$")
    plt.title(f"Przekrój Poincaré z tłumieniem, K={K}")
    plt.grid(True)
    plt.savefig(f"poincare_zad_2/K_{K}_2.png")
    plt.close()
