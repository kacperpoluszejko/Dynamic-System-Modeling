# import numpy as np
# import matplotlib.pyplot as plt

# # zakres parametru m
# m = np.linspace(0, 3, 200)


# Re_lambda1 = np.zeros_like(m)
# Re_lambda2 = np.zeros_like(m)
# Im_lambda1 = np.ones_like(m)
# Im_lambda2 = -np.ones_like(m)

# plt.figure(figsize=(8, 6))

# # --- wykres części rzeczywistej ---
# plt.subplot(2, 1, 1)
# plt.plot(m, Re_lambda1, label=r'$\Re \lambda_1$')
# plt.plot(m, Re_lambda2, '--', label=r'$\Re \lambda_2$')
# plt.xlabel(r'$m$')
# plt.ylabel(r'$\Re \lambda$')
# plt.title(r'$\varepsilon = 0$')
# plt.grid(True)
# plt.legend()

# # --- wykres części urojonej ---
# plt.subplot(2, 1, 2)
# plt.plot(m, Im_lambda1, label=r'$\Im \lambda_1$')
# plt.plot(m, Im_lambda2, '--', label=r'$\Im \lambda_2$')
# plt.xlabel(r'$m$')
# plt.ylabel(r'$\Im \lambda$')
# plt.grid(True)
# plt.legend()

# plt.tight_layout()
# plt.savefig("Rys_1.png")
# plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Zakres parametru m
m = np.linspace(0.0, 3.0, 500)

# Parametr eps
eps = 0.5

# Element (2,2) Jacobiego: a = eps * (m^2 - 1)
a = eps * (m**2 - 1.0)

# Równanie charakterystyczne: λ^2 - a λ + 1 = 0
# Dyskryminant: Δ = a^2 - 4
disc = a**2 - 4.0

# Wartości własne:
# λ_{1,2} = (a ± sqrt(a^2 - 4)) / 2
lambda1 = (a + np.sqrt(disc + 0j)) / 2.0   # +0j: pierwiastek zespolony
lambda2 = (a - np.sqrt(disc + 0j)) / 2.0

# Części rzeczywiste i urojone
Re1 = np.real(lambda1)
Re2 = np.real(lambda2)
Im1 = np.imag(lambda1)
Im2 = np.imag(lambda2)

# ---- RYSOWANIE ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

# Część rzeczywista
ax1.plot(m, Re1, label=r'$\Re \lambda_1$')
ax1.plot(m, Re2, label=r'$\Re \lambda_2$')
ax1.axhline(0.0, linewidth=0.8)

ax1.set_ylabel(r'$\Re \lambda$')
ax1.set_title(
    r'$\varepsilon = \frac{1}{2}$'
)
ax1.grid(True)
ax1.legend(loc='best')

# Część urojona
ax2.plot(m, Im1, label=r'$\Im \lambda_1$')
ax2.plot(m, Im2, label=r'$\Im \lambda_2$')
ax2.axhline(0.0, linewidth=0.8)

ax2.set_xlabel(r'$m$')
ax2.set_ylabel(r'$\Im \lambda$')
ax2.grid(True)
ax2.legend(loc='best')

plt.tight_layout()
plt.savefig("Rys_2.png")
plt.show()
