import numpy as np
import matplotlib.pyplot as plt

r = 3.569945672
N = 1000000
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

    if ln_eps.size < 2:
        return np.nan, np.nan

    coeffs, cov = np.polyfit(ln_eps, ln_Z, 1, cov=True)
    return coeffs[0], np.sqrt(cov[0, 0])


q_vals = np.concatenate((
    np.arange(-10.0, 0.1, 0.5),
    np.arange(0.5, 10.1, 0.5)
))

k_vals = np.arange(10, 25)

tau_vals = []
tau_errs = []

for q in q_vals:
    t, dt = tau_q_1d_with_error(x, q, k_vals)
    tau_vals.append(t)
    tau_errs.append(dt)

tau_vals = np.array(tau_vals)
tau_errs = np.array(tau_errs)

D_vals = np.full_like(q_vals, np.nan, dtype=float)
D_errs = np.full_like(q_vals, np.nan, dtype=float)

mask = q_vals != 1
D_vals[mask] = tau_vals[mask] / (q_vals[mask] - 1)
D_errs[mask] = tau_errs[mask] / np.abs(q_vals[mask] - 1)

dq = 1e-3

tau_m, dtau_m = tau_q_1d_with_error(x, 1 - dq, k_vals)
tau_p, dtau_p = tau_q_1d_with_error(x, 1 + dq, k_vals)

D1 = 0.5 * (tau_m / (-dq) + tau_p / dq)

D1_err = 0.5 * np.sqrt(
    (dtau_m / dq)**2 +
    (dtau_p / dq)**2
)

i1 = np.argmin(np.abs(q_vals - 1))
D_vals[i1] = D1
D_errs[i1] = D1_err


i1 = np.argmin(np.abs(q_vals - 1))
D_vals[i1] = D1

i0 = np.argmin(np.abs(q_vals - 0))
i1 = np.argmin(np.abs(q_vals - 1))
i2 = np.argmin(np.abs(q_vals - 2))

print(D_vals[i0])
print(D_vals[i1])
print(D_vals[i2])

print(D_errs[i0])
print(D_errs[i1])
print(D_errs[i2])


plt.figure()
plt.errorbar(q_vals, tau_vals, yerr=tau_errs, fmt='o')
plt.xlabel("q")
plt.ylabel("tau(q)")
plt.savefig("Lab_10/tau.png")
plt.show()

plt.figure()
plt.errorbar(q_vals, D_vals, yerr=D_errs, fmt='o')
plt.xlabel("q")
plt.ylabel("D(q)")
plt.savefig("Lab_10/D_q.png")
plt.show()
