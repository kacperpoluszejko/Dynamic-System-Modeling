import numpy as np
import matplotlib.pyplot as plt

# Wczytanie danych
data1 = np.loadtxt("Lab_2/wynik_1.txt")
data2 = np.loadtxt("Lab_2/wynik_2.txt")
data3 = np.loadtxt("Lab_2/wynik_3.txt")
data4 = np.loadtxt("Lab_2/wynik_4.txt")
data5 = np.loadtxt("Lab_2/wynik_5.txt")
data6 = np.loadtxt("Lab_2/wynik_6.txt")
data7 = np.loadtxt("Lab_2/wynik_7.txt")
data8 = np.loadtxt("Lab_2/wynik_8.txt")
data9 = np.loadtxt("Lab_2/wynik_9.txt")
data10 = np.loadtxt("Lab_2/wynik_10.txt")
data11= np.loadtxt("Lab_2/wynik_11.txt")
data12 = np.loadtxt("Lab_2/wynik_12.txt")
data13 = np.loadtxt("Lab_2/wynik_13.txt")
data14 = np.loadtxt("Lab_2/wynik_14.txt")
data15 = np.loadtxt("Lab_2/wynik_15.txt")
data16 = np.loadtxt("Lab_2/wynik_16.txt")




# Rozpakowanie kolumn (t, y_num, y_exact, abs_err, rel_err)
t1, y1_num, y1_exact, abs1, rel1 = data1.T
t2, y2_num, y2_exact, abs2, rel2 = data2.T
t3, y3_num, y3_exact, abs3, rel3 = data3.T
t4, y4_num, y4_exact, abs4, rel4 = data4.T
t5, y5_num, y5_exact, abs5, rel5 = data5.T
t6, y6_num, y6_exact, abs6, rel6 = data6.T
t7, y7_num, y7_exact, abs7, rel7 = data7.T
t8, y8_num, y8_exact, abs8, rel8 = data8.T
t9, y9_num, y9_exact, abs9, rel9 = data9.T
t10, y10_num, y10_exact, abs10, rel10 = data10.T
t11, y11_num, y11_exact, abs11, rel11 = data11.T
t12, y12_num, y12_exact, abs12, rel12 = data12.T
t13, y13_num, y13_exact, abs13, rel13 = data13.T
t14, y14_num, y14_exact, abs14, rel14 = data14.T
t15, y15_num, y15_exact, abs15, rel15 = data15.T
t16, y16_num, y16_exact, abs16, rel16 = data16.T


# ------------------------------
# 1️⃣ Wykres y(t) – numeryczne i analityczne
# ------------------------------
plt.figure(figsize=(8, 5))
plt.plot(t1,  y1_num,  label='y0=1 num',  color='blue')
plt.plot(t2,  y2_num,  label='y0=2 num',  color='orange')
plt.plot(t3,  y3_num,  label='y0=3 num',  color='green')
plt.plot(t4,  y4_num,  label='y0=4 num',  color='red')
plt.plot(t5,  y5_num,  label='y0=5 num',  color='purple')
plt.plot(t6,  y6_num,  label='y0=6 num',  color='brown')
plt.plot(t7,  y7_num,  label='y0=7 num',  color='pink')
plt.plot(t8,  y8_num,  label='y0=8 num',  color='gray')
plt.plot(t9,  y9_num,  label='y0=9 num',  color='olive')
plt.plot(t10, y10_num, label='y0=10 num', color='cyan')
plt.plot(t11, y11_num, label='y0=11 num', color='teal')
plt.plot(t12, y12_num, label='y0=12 num', color='gold')
plt.plot(t13, y13_num, label='y0=13 num', color='navy')
plt.plot(t14, y14_num, label='y0=14 num', color='lime')
plt.plot(t15, y15_num, label='y0=15 num', color='magenta')
plt.plot(t16, y16_num, label='y0=16 num', color='black')

plt.xlabel("t")
plt.ylabel("x(t)")
plt.ylim(-3, 3)
plt.grid(True)
plt.savefig("wykr_2.png")
plt.show()



