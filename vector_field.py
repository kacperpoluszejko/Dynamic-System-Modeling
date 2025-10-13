import numpy as np
import matplotlib.pyplot as plt

# Define the function dy/dx = f(x, y)
def f(x, y):
    return x + y

# Create a grid of points
x = np.linspace(-3, 3, 20)
y = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x, y)

# Compute slopes
U = 1  # dx = 1 for direction field
V = f(X, Y)

# Normalize the arrows for better visualization
N = np.sqrt(U**2 + V**2)
U2, V2 = U/N, V/N

# Plot the direction field
plt.figure(figsize=(8, 6))
plt.quiver(X, Y, U2, V2, angles='xy')

# Plot a few isoclines for m = -2, -1, 0, 1, 2
m_values = [-2, -1, 0, 1, 2]
for m in m_values:
    y_iso = -x + m
    plt.plot(x, y_iso, label=f"izoklina m={m}")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Izokliny i pole kierunków dla równania y' = x + y")
plt.legend()
plt.grid(True)
plt.show()
