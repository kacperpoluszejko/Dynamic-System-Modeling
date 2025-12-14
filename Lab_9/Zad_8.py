import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("Lab_9/poincare_double_a_1.1.txt")
points = data[:, :2]

np.random.seed(0)
Nmax = 5000
if len(points) > Nmax:
    idx = np.random.choice(len(points), Nmax, replace=False)
    points = points[idx]

N = len(points)

def correlation_integral(points, r_values):
    C = []
    for r in r_values:
        count = 0
        for i in range(N):
            dist = np.linalg.norm(points[i+1:] - points[i], axis=1)
            count += np.sum(dist < r)
        C.append(2 * count / (N * (N - 1)))
    return np.array(C)

r_values = np.logspace(-2.5, -0.8, 15)
C_r = correlation_integral(points, r_values)

X = np.log(r_values)
Y = np.log(C_r)

coeffs = np.polyfit(X, Y, 1)
D2 = coeffs[0]
C0 = coeffs[1]

Y_fit = D2 * X + C0

residuals = Y - Y_fit
sigma_D2 = np.sqrt(
    np.sum(residuals**2) /
    ((len(X) - 2) * np.sum((X - np.mean(X))**2))
)

print(f"D2 = {D2:.3f} ± {sigma_D2:.3f}")

plt.scatter(X, Y)
plt.plot(X, Y_fit)
plt.xlabel("log r")
plt.ylabel("log C(r)")
plt.tight_layout()
plt.savefig("Dopasowanie_kor_2.png")
plt.show()

#D2 = 1.211 ± 0.003 - 1.4
#D2 = 0.892 ± 0.003 - 1.1