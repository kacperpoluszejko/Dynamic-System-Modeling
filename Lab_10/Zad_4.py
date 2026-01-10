import numpy as np
import matplotlib.pyplot as plt

r = 3.569945672
N = 100000
x_old = 0.5
x_table = []

for i in range(N):
    x_new = r * x_old * (1 - x_old)
    if i > 1000:
        x_table.append(x_new)
    x_old = x_new

x = np.array(x_table)
x = (x - x.min()) / (x.max() - x.min())


def Z_q_eps_1d(x, eps, q):
    n = int(1.0 / eps)
    ix = np.floor(x * n).astype(int)
    _, counts = np.unique(ix, return_counts=True)
    mu = counts / np.sum(counts)
    if q == 1:
        return np.sum(mu * np.log(mu))
    else:
        return np.sum(mu**q)
    

def tau_q_1d_with_error(x, q, k_vals):
    ln_eps = []
    ln_Z = []

    for k in k_vals:
        eps = 1.5**(-k)
        Z = Z_q_eps_1d(x, eps, q)
        if np.isfinite(Z) and Z > 0:
            ln_eps.append(np.log(eps))
            ln_Z.append(np.log(Z))

    ln_eps = np.array(ln_eps)
    ln_Z = np.array(ln_Z)

    coeffs, cov = np.polyfit(ln_eps, ln_Z, 1, cov=True)
    tau = coeffs[0]
    tau_err = np.sqrt(cov[0, 0])

    return tau, tau_err


q_vals = np.concatenate((
    np.arange(-10.0, 0.1, 0.5),
    np.arange(0.5, 10.1, 0.5)
))

k_vals = np.arange(4, 12)


tau_vals = []
tau_errs = []

for q in q_vals:
    t, dt = tau_q_1d_with_error(x, q, k_vals)
    tau_vals.append(t)
    tau_errs.append(dt)


import matplotlib.pyplot as plt

plt.errorbar(q_vals, tau_vals, yerr=tau_errs, fmt='o')
plt.xlabel("q")
plt.ylabel("tau(q)")
plt.show()
