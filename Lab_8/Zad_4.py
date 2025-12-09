import numpy as np
import matplotlib.pyplot as plt
import imageio
import io
from numba import njit


@njit
def poincare_map(K, theta0, L0_list, N):
    M = len(L0_list)
    theta_points = np.zeros(M * N)
    L_points = np.zeros(M * N)

    idx = 0
    for j in range(M):
        theta = theta0
        L = L0_list[j]
        for _ in range(N):
            theta_points[idx] = theta % (2*np.pi)
            L_points[idx] = L

            L_old = L
            theta_old = theta


            L = L_old + K * np.sin(theta_old)
            theta = theta_old + L

            idx += 1

    return theta_points, L_points




theta0 = np.pi
alpha = np.arange(0, 1, 0.02)
L0_list = alpha * 2 * np.pi
N = 2000

K_min = 0.0
K_max = 2.0
K_step = 0.01

K_anim = np.arange(K_min, K_max + K_step, K_step)

frames = []


for K in K_anim:

    theta_points, L_points = poincare_map(K, theta0, L0_list, N)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(theta_points, L_points, s=1)
    ax.set_xlabel(r"$\theta \;(\mathrm{mod}\; 2\pi)$")
    ax.set_ylabel(r"$L$")
    ax.set_title(f"Poincaré map, K = {K:.2f}")
    ax.grid(True)


    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    frames.append(imageio.v2.imread(buf))
    plt.close(fig)


imageio.mimsave("poincare.gif", frames, duration=0.05, loop=0)


