import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("lab_9\henon_a_float0.500000.txt")
x = data[:, 0]
y = data[:, 1]

data1 = np.loadtxt("lab_9\henon_a_float1.100000.txt")
x1 = data1[:, 0]
y1 = data1[:, 1]

data2 = np.loadtxt("lab_9\henon_a_float1.250000.txt")
x2 = data2[:, 0]
y2 = data2[:, 1]

data3 = np.loadtxt("lab_9\henon_a_float1.400000.txt")
x3 = data3[:, 0]
y3 = data3[:, 1]




plt.scatter(range(len(x)), x, s=2)
plt.scatter(range(len(y)), y, s=2)
plt.savefig("a_1_float.png")
plt.show()



plt.scatter(range(len(x)), x1, s=2)
plt.scatter(range(len(y)), y1, s=2)
plt.savefig("a_2_float.png")
plt.show()


plt.scatter(range(len(x)), x2, s=2)
plt.scatter(range(len(y)), y2, s=2)
plt.savefig("a_3_float.png")
plt.show()


plt.scatter(range(len(x)), x3, s=2)
plt.scatter(range(len(y)), y3, s=2)
plt.savefig("a_4_float.png")
plt.show()
