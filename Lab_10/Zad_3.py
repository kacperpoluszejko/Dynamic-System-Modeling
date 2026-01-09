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

q_vals = np.array([-1, 0, 1, 2])
tau_num_vals = []
tau_exact_vals = []

for q in q_vals:
    t_num, t_ex = calc_tau(q)
    tau_num_vals.append(t_num)
    tau_exact_vals.append(t_ex)

plt.plot(q_vals, tau_num_vals, marker='o', linestyle='-', label='numeryczne')
plt.plot(q_vals, tau_exact_vals, marker='s', linestyle='--', label='analityczne')
plt.xlabel("q")
plt.ylabel("tau(q)")
plt.title("p = 1/4")
plt.legend()
plt.savefig("p_2.png")
plt.show()



