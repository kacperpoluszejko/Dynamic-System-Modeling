import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt("wynik1.txt")
data2 = np.loadtxt("wynik2.txt")
data3 = np.loadtxt("wynik3.txt")
data4 = np.loadtxt("wynik4.txt")


t1 = data1[:, 0]
y1 = data1[:, 1]
t2 = data2[:, 0]
y2 = data2[:, 1]
t3 = data3[:, 0]
y3 = data3[:, 1]
t4 = data4[:, 0]
y4 = data4[:, 1]

plt.figure(figsize=(8, 5))

plt.plot(t1, y1, label='y[0] = 0', color='blue')
plt.plot(t2, y2, label='y[0] = 0.5', color='red')
plt.plot(t3, y3, label='y[0] = 1', color='green')
plt.plot(t4, y4, label='y[0] = 2', color='cyan')
plt.xlim(0, 1)
plt.ylim(0, 20)

plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
