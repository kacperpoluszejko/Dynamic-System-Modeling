import numpy as np
import matplotlib.pyplot as plt
import os

K_table = np.array([0.5, 0.971635, 5.0])
os.makedirs("poincare", exist_ok=True)

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

            L = L_old + K * np.sin(theta_old)
            theta = theta_old + L

    plt.figure(figsize=(6,6))
    plt.scatter(points_theta, points_L, s=1)
    plt.xlabel(r"$\theta \;(\mathrm{mod}\; 2\pi)$")
    plt.ylabel(r"$L$")
    plt.title(f"Przekrój Poincaré, K={K}")
    plt.grid(True)
    plt.savefig(f"poincare/K_{K}.png")
    plt.close()
