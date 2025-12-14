import numpy as np
import matplotlib.pyplot as plt

a_vals = [1.40]

for a in a_vals:
    data_d = np.loadtxt(f"Lab_9/poincare_double_a_{a}.txt")

    x_d, y_d = data_d[:,0], data_d[:,1]

    plt.figure(figsize=(6,5))
    plt.scatter(x_d, y_d, s=0.1, label="double", alpha=0.7)
    plt.xlim(0.25, 0.35)   
    plt.ylim(0.17, 0.26)
    plt.title(f"Poincaré2: a = {a}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.gca().set_aspect('equal', 'box')
    plt.savefig(f"poincare_{a}v4.png")
    plt.show()




