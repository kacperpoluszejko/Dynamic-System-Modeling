import numpy as np
import matplotlib.pyplot as plt

p1 = np.linspace(-1, 3, 400)
p2 = np.linspace(3, 6, 400)

x1_left = np.full_like(p1, 1.0)
x1_right = np.full_like(p2, 1.0)

x2_left = -1 + np.sqrt(1 + p1)
x2_right = -1 + np.sqrt(1 + p2)

x3 = -1 - np.sqrt(1 + np.linspace(-1, 6, 500))
p3 = np.linspace(-1, 6, 500)

plt.figure(figsize=(8,5))
plt.plot(p1, x1_left, linestyle='--', label=r'$x^*=1$')
plt.plot(p2, x1_right, linestyle='-')
plt.plot(p1, x2_left, linestyle='-', label=r'$x^*=-1+\sqrt{1+p}$')
plt.plot(p2, x2_right, linestyle='--')
plt.plot(p3, x3, linestyle='--', label=r'$x^*=-1-\sqrt{1+p}$')
plt.xlabel('p')
plt.ylabel(r'$x^*$')
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.savefig('diagram_bifurkacyjny.png', dpi=200)
# plt.show()
