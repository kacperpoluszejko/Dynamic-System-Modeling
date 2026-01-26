import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("Lorenz_attractor/lyapunov_vs_rho.txt")
rho = data[:, 0]
lam = data[:, 1]

plt.plot(rho, lam)
plt.axhline(0.0, linewidth=0.8)
plt.xlabel(r"$\rho$")
plt.ylabel(r"$\lambda_{\max}(\rho)$")
plt.grid(True)
plt.tight_layout()
plt.savefig("lyapunov_vs_rho.png", dpi=300)
plt.show()
