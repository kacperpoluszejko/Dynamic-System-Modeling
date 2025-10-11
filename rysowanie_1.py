import numpy as np
import matplotlib.pyplot as plt

# Wczytanie danych
data1 = np.loadtxt("wynik1.txt")
data2 = np.loadtxt("wynik2.txt")
data3 = np.loadtxt("wynik3.txt")
data4 = np.loadtxt("wynik4.txt")

# Rozpakowanie kolumn (t, y_num, y_exact, abs_err, rel_err)
t1, y1_num, y1_exact, abs1, rel1 = data1.T
t2, y2_num, y2_exact, abs2, rel2 = data2.T
t3, y3_num, y3_exact, abs3, rel3 = data3.T
t4, y4_num, y4_exact, abs4, rel4 = data4.T

# ------------------------------
# 1️⃣ Wykres y(t) – numeryczne i analityczne
# ------------------------------
plt.figure(figsize=(8, 5))
plt.plot(t1, y1_num, label='y0=0 num', color='blue')
plt.plot(t1, y1_exact, '--', color='blue', alpha=0.6)

plt.plot(t2, y2_num, label='y0=0.5 num', color='red')
plt.plot(t2, y2_exact, '--', color='red', alpha=0.6)

plt.plot(t3, y3_num, label='y0=1 num', color='green')
plt.plot(t3, y3_exact, '--', color='green', alpha=0.6)

plt.plot(t4, y4_num, label='y0=2 num', color='cyan')
plt.plot(t4, y4_exact, '--', color='cyan', alpha=0.6)

plt.xlim(0, 1)
plt.ylim(0, 20)
plt.xlabel('t')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.title('Porównanie rozwiązania numerycznego i analitycznego')
plt.tight_layout()
plt.show()

# ------------------------------
# 2️⃣ Wykres błędu bezwzględnego
# ------------------------------
plt.figure(figsize=(8, 5))
plt.semilogy(t1, abs1 + 1e-16,"x", label='y0=0', color='blue')
plt.semilogy(t2, abs2,"x", label='y0=0.5', color='red')
plt.semilogy(t3, abs3,"x", label='y0=1', color='green')
plt.semilogy(t4, abs4,"x", label='y0=2', color='cyan')
plt.xlabel('t')
plt.ylabel('Błąd bezwzględny |y_num - y_exact|')
plt.legend()
plt.grid(True)
plt.ylim(0, 1e-8)
plt.title('Błąd bezwzględny')
plt.tight_layout()
plt.show()

# ------------------------------
# 3️⃣ Wykres błędu względnego (skala logarytmiczna)
# ------------------------------
plt.figure(figsize=(8, 5))
plt.plot(t1, rel1, label='y0=0', color='blue')
plt.plot(t2, rel2, label='y0=0.5', color='red')
plt.plot(t3, rel3, label='y0=1', color='green')
plt.plot(t4, rel4, label='y0=2', color='cyan')
plt.xlabel('t')
plt.ylabel('Błąd względny')
plt.yscale('log')
plt.legend()
plt.grid(True, which='both')
plt.title('Błąd względny (skala log)')
plt.tight_layout()
plt.show()
