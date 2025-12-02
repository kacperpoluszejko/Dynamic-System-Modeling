import numpy as np
import matplotlib.pyplot as plt
import os

K_table = np.array([0.5, 0.971635, 5.0])
theta_0_table = np.array([0, 0.2*np.pi, 0.2*2*np.pi])
L_0_table = np.array([0.1*2*np.pi, 0.2*2*np.pi, 0.65*2*np.pi])

N = 1000
n_table = np.arange(N+1)

os.makedirs("wyniki", exist_ok=True)

for K in K_table:
    for i in range(len(theta_0_table)):

        theta = theta_0_table[i]
        L = L_0_table[i]

        theta_table = np.zeros(N+1)
        L_table = np.zeros(N+1)

        for n in range(N+1):
            theta_table[n] = theta
            L_table[n] = L
            
            L = L + K * np.sin(theta)
            theta = theta + L + K * np.sin(theta)

        plt.figure()
        plt.plot(n_table, theta_table)
        plt.xlabel("n")
        plt.ylabel(r"$\theta_n$")
        plt.title(f"Theta: K={K}, start {i}")
        plt.grid(True)
        plt.savefig(f"wyniki/theta_K_{K}_start_{i}.png")
        plt.close()

        plt.figure()
        plt.plot(n_table, L_table)
        plt.xlabel("n")
        plt.ylabel(r"$L_n$")
        plt.title(f"L: K={K}, start {i}")
        plt.grid(True)
        plt.savefig(f"wyniki/L_K_{K}_start_{i}.png")
        plt.close()
