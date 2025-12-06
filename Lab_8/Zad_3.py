import numpy as np
import matplotlib.pyplot as plt
import os

K_table = np.array([0.5, 0.971635, 5.0])
theta_0_table = np.array([0, 0.2*np.pi, 0.2*2*np.pi])
L_0_table = np.array([0.1*2*np.pi, 0.2*2*np.pi, 0.65*2*np.pi])

b = 0.01
N = 1000
n_table = np.arange(N+1)

os.makedirs("wyniki_zad3", exist_ok=True)

for K in K_table:

    theta_hist = np.zeros((3, N+1))
    L_hist = np.zeros((3, N+1))

    theta = theta_0_table.copy()
    L = L_0_table.copy()

    for n in range(N+1):
        theta_hist[:, n] = theta
        L_hist[:, n] = L

        L_old = L.copy()
        theta_old = theta.copy()

        L = (L_old + K * np.sin(theta_old)) * np.exp(-b)
        theta = theta_old + (L_old + K * np.sin(theta_old)) * ((1 - np.exp(-b)) / b)

    plt.figure()
    for i in range(3):
        label = fr"$\theta_0={theta_0_table[i]:.3f},\;L_0={L_0_table[i]:.3f}$"
        plt.plot(n_table, theta_hist[i], label=label)
    plt.xlabel("n")
    plt.ylabel(r"$\theta_n$")
    plt.title(f"Theta, K={K}")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"wyniki_zad3/theta_K_{K}3.png")
    plt.close()

    plt.figure()
    for i in range(3):
        label = fr"$\theta_0={theta_0_table[i]:.3f},\;L_0={L_0_table[i]:.3f}$"
        plt.plot(n_table, L_hist[i], label=label)
    plt.xlabel("n")
    plt.ylabel(r"$L_n$")
    plt.title(f"L, K={K}")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"wyniki_zad3/L_K_{K}3.png")
    plt.close()
