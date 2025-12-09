import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("Lab_9/bifurcation.txt")

a = data[:, 0]
x = data[:, 1]

plt.figure(figsize=(10, 6))
plt.scatter(a, x, s=0.001, color='black')
plt.xlabel("a")
plt.ylabel("x_n")
plt.title("Diagram bifurkacyjny")
plt.tight_layout()
plt.savefig("bifurkacje.png")
plt.show()
