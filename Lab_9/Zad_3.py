import numpy as np
import matplotlib.pyplot as plt

def autocorrelation(x, max_lag):
    x = x - np.mean(x)
    result = np.correlate(x, x, mode='full')
    ac = result[result.size // 2:]
    ac = ac[:max_lag]
    return ac / ac[0]

a_values = [0.50, 1.10, 1.25, 1.40]

plt.figure(figsize=(10,6))

for a in a_values:
    data = np.loadtxt(f"Lab_9\henon_a_{a}.txt")
    x = data[:,0]
    
    R = autocorrelation(x, max_lag=20)
    plt.plot(R, label=f"a = {a}")

plt.title("Autokorelacja x_n dla różnych wartości parametru a")
plt.xlabel("Opóźnienie k")
plt.ylabel("R(k)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Autokorelacja.png")
plt.show()
