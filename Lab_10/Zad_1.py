import numpy as np
import matplotlib.pyplot as plt

r = 3.569945672
N = 100000
x_old = 0.5
x_table = []

for i in range(N):
    x_new = r * x_old * (1 - x_old)
    if i > 1000:
        x_table.append(x_new)
    x_old = x_new

x = np.array(x_table)
x = (x - x.min()) / (x.max() - x.min())


def box_counting_1d(x, eps_list):
    N_boxes = []
    for eps in eps_list:
        n = int(1.0 / eps)
        ix = np.floor(x * n).astype(int)
        boxes = np.unique(ix)
        N_boxes.append(len(boxes))
    return np.array(N_boxes)

eps_list = np.logspace(-1.5, -3.0, 12)

N_eps = box_counting_1d(x, eps_list)

X = np.log(1.0 / eps_list)
Y = np.log(N_eps)

coeffs = np.polyfit(X, Y, 1)
D = coeffs[0]
C = coeffs[1]

Y_fit = D * X + C

N = len(X)
residuals = Y - Y_fit

sigma_D = np.sqrt(
    np.sum(residuals**2) /
    ((N - 2) * np.sum((X - np.mean(X))**2))
)

print(f"Wymiar fraktalny d_f = {D:.3f} ± {sigma_D:.3f}")

plt.scatter(X, Y)
plt.plot(X, Y_fit)
plt.xlabel("log(1/ε)")
plt.ylabel("log N(ε)")
plt.tight_layout()
plt.savefig("Dopasowanie.png")
plt.show()
