import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-0.2, 1.2, 300)
V_k1 = -(x**2 / 2 - x**3 / 3)
V_km1 = +(x**2 / 2 - x**3 / 3)

plt.plot(x, V_k1, label='k=1')
plt.plot(x, V_km1, label='k=-1')
plt.xlabel('x')
plt.ylabel('V(x)')
plt.legend()
plt.grid(True)
plt.savefig("V(x).png")
plt.show()
