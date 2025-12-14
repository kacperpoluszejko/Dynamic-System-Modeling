import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("Lab_9/poincare_double_a_1.1.txt")
x = data[:, 0]
y = data[:, 1]


x = (x - x.min()) / (x.max() - x.min())
y = (y - y.min()) / (y.max() - y.min())



def box_counting(x, y, eps_list):
    N_boxes = []

    for eps in eps_list:
        n = int(1.0 / eps)

        ix = np.floor(x * n).astype(int)
        iy = np.floor(y * n).astype(int)

        boxes = set(zip(ix, iy))
        N_boxes.append(len(boxes))

    return np.array(N_boxes)

eps_list = np.logspace(-1.5, -3.0, 12)

N_eps = box_counting(x, y, eps_list)


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


print(f"Wymiar fraktalny D = {D:.3f} ± {sigma_D:.3f}")


plt.scatter(X, Y, label="dane")
plt.plot(X, Y_fit, label="dopasowanie")
plt.xlabel("log(1/ε)")
plt.ylabel("log N(ε)")
plt.title("Box-counting – wymiar fraktalny (a = 1.1)")
plt.legend()
plt.tight_layout()
plt.savefig("Dopaowanie_2.png")
plt.show()


#Wymiar fraktalny D = 1.226 ± 0.006
#Wymiar fraktalny D = 1.127 ± 0.005 - 1.1