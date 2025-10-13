import numpy as np
import matplotlib.pyplot as plt

# ===== Wczytanie danych =====
data = np.loadtxt("Lab_2/wynik_lv.txt")

t = data[:, 0]
x = data[:, 1]
y = data[:, 2]
H = data[:, 3]

# ===== Wykres 1: trajektoria w przestrzeni fazowej =====
plt.figure(figsize=(6,6))
plt.plot(x, y, color='blue')
plt.scatter([x[0]], [y[0]], color='red', label='start')
plt.scatter([x[-1]], [y[-1]], color='green', label='koniec')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trajektoria w przestrzeni fazowej (x,y)\n układ: x' = x(1-y), y' = y(x-1)")
plt.legend()
plt.grid(True)
plt.axis("equal")

# ===== Wykres 2: ewolucja zmiennych w czasie =====
plt.figure(figsize=(8,4))
plt.plot(t, x, label="x(t)")
plt.plot(t, y, label="y(t)")
plt.xlabel("t")
plt.ylabel("x, y")
plt.title("Ewolucja x(t) i y(t) w czasie")
plt.legend()
plt.grid(True)

# ===== Wykres 3: zachowana wielkość H(x,y) =====
plt.figure(figsize=(8,4))
plt.plot(t, H, color='purple')
plt.xlabel("t")
plt.ylabel("H(x,y)")
plt.title("Zachowana wielkość H(x,y) = x - ln(x) + y - ln(y)")
plt.grid(True)

plt.show()
