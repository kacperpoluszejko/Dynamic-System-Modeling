
import numpy as np
import matplotlib.pyplot as plt


m = np.linspace(0.0, 2.0, 400)

x_stable =  +m   # x* = +m  (stabilny)
x_unstable = -m  # x* = -m  (niestabilny)

plt.figure(figsize=(8, 5))

plt.plot(m, x_stable,  linestyle='-',  label=r'$x^* = +m$ (stabilny)')
plt.plot(m, x_unstable, linestyle='--', label=r'$x^* = -m$ (niestabilny)')


# plt.scatter([0], [0], marker='o', zorder=3)



plt.xlabel('m')
plt.ylabel(r'$x^*$')

plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()


plt.savefig('bifurkacja.png', dpi=200)
plt.show()
