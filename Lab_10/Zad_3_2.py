import numpy as np
import matplotlib.pyplot as plt

p = 1/4
k = 6

def calc_tau(q):
    mi = [1.0]
    Z_table = []
    eps_table = []

    for n in range(1, k + 1):
        mi = [x*p for x in mi] + [x*(1-p) for x in mi]
        Z_table.append(sum(x**q for x in mi))
        eps_table.append(3**(-n))

    ln_eps = np.log(eps_table)
    ln_Z = np.log(Z_table)

    tau_num = np.polyfit(ln_eps, ln_Z, 1)[0]
    tau_exact = -np.log(p**q + (1 - p)**q) / np.log(3)

    return tau_num, tau_exact

def calc_Dq(q):
    if q == 1:
        dq = 1e-4
        t_plus, _ = calc_tau(1 + dq)
        t_minus, _ = calc_tau(1 - dq)
        D_num = (t_plus - t_minus) / (2 * dq) #liczymy to z Taylora
        D_exact = -(p*np.log(p) + (1-p)*np.log(1-p)) / np.log(3)
        return D_num, D_exact
    else:
        tn, te = calc_tau(q)
        return tn / (q - 1), te / (q - 1)


q_vals = np.array([-1, 0, 1, 2])

D_num_vals = []
D_exact_vals = []

for q in q_vals:
    dnum, dex = calc_Dq(q)
    D_num_vals.append(dnum)
    D_exact_vals.append(dex)

plt.plot(q_vals, D_num_vals, marker='o', linestyle='-', label='numeryczne')
plt.plot(q_vals, D_exact_vals, marker='s', linestyle='--', label='analityczne')
plt.xlabel("q")
plt.ylabel("D_q")
plt.title("p=1/4")
plt.legend()
plt.savefig("Dq_2.png")
plt.show()
