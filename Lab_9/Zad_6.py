import numpy as np
import matplotlib.pyplot as plt

a_vals = [0.50, 1.10, 1.25, 1.40]

for a in a_vals:
    data_d = np.loadtxt(f"Lab_9/poincare_multi_double_a_{a}.txt")
    data_f = np.loadtxt(f"Lab_9/poincare_multi_float_a_{a}.txt")

    x_d, y_d = data_d[:,0], data_d[:,1]
    x_f, y_f = data_f[:,0], data_f[:,1]

    plt.figure(figsize=(6,5))
    plt.scatter(x_d, y_d, s=1, label="double", alpha=0.7)
    plt.scatter(x_f, y_f, s=1, label="float", alpha=0.7)
    plt.title(f"Poincaré: a = {a}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"poincare_multi_{a}.png")
    plt.show()