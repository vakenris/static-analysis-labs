import math
import pandas as pd
import matplotlib.pyplot as plt


def calc_asymmetry(data, mean, std):
    """Вычисление центрального момента 3-го порядка и коэффициента асимметрии"""
    n = len(data)
    m3 = sum((x - mean) ** 3 for x in data) / n
    asym = m3 / (std ** 3)
    return m3, asym

def calc_kurtosis(data, mean, std):
    """Вычисление центрального момента 4-го порядка и коэффициента эксцесса"""
    n = len(data)
    m4 = sum((x - mean) ** 4 for x in data) / n
    ex = (m4 / (std ** 4)) - 3
    return m4, ex


ages_series = pd.read_csv("../Москва_2021.txt", header=None, names=["age"])["age"]
ages_list = ages_series.tolist()
n = len(ages_list)

mean = sum(ages_list) / n
var = sum((x - mean) ** 2 for x in ages_list) / n
std = math.sqrt(var)


m3, asym = calc_asymmetry(ages_list, mean, std)
m4, ex = calc_kurtosis(ages_list, mean, std)


print(f"M(X) = {mean:.4f}")
print(f"σ(X) = {std:.4f}")
print(f"m3 = {m3:.4f}")
print(f"m4 = {m4:.4f}")
print(f"A_s = {asym:.4f}")
print(f"E_k = {ex:.4f}")

if asym > 0:
    print("Вывод: асимметрия положительная (Правосторонняя).")
elif asym < 0:
    print("Вывод: асимметрия отрицательная (Левосторонняя).")
else:
    print("Вывод: Нормальное распределение (Симметричное)")

if ex > 0:
    print("Вывод: Островершинное распределение")
elif ex < 0:
    print("Вывод: Плосковершинное распределение")
else:
    print("Вывод: Нормальное распределение")
print()


print("Правило трёх сигм")

l1, r1 = mean - std, mean + std
l2, r2 = mean - 2 * std, mean + 2 * std
l3, r3 = mean - 3 * std, mean + 3 * std

c1 = sum(1 for x in ages_list if l1 <= x <= r1)
c2 = sum(1 for x in ages_list if l2 <= x <= r2)
c3 = sum(1 for x in ages_list if l3 <= x <= r3)

p1 = (c1 / n) * 100
p2 = (c2 / n) * 100
p3 = (c3 / n) * 100

p1_th, p2_th, p3_th = 68.26, 95.44, 99.73

dev1 = abs(p1 - p1_th)
dev2 = abs(p2 - p2_th)
dev3 = abs(p3 - p3_th)

print(f"1σ [{l1:.2f}; {r1:.2f}] → кол-во: {c1} | {p1:.2f}% (теор. {p1_th}%, откл. {dev1:.2f}%)")
print(f"2σ [{l2:.2f}; {r2:.2f}] → кол-во: {c2} | {p2:.2f}% (теор. {p2_th}%, откл. {dev2:.2f}%)")
print(f"3σ [{l3:.2f}; {r3:.2f}] → кол-во: {c3} | {p3:.2f}% (теор. {p3_th}%, откл. {dev3:.2f}%)")
print()

delta = 0.5
if dev1 <= delta and dev2 <= delta and dev3 <= delta:
    print(f"Для допустимой погрешности δ = {delta}% правило трех сигм выполняется, следовательно, распределение случайной величины «возраст» является нормальным.")
else:
    print(f"Для допустимой погрешности δ = {delta}% правило трех сигм не выполняется, следовательно, распределение случайной величины «возраст» не является нормальным.")


ecdf = ages_series.value_counts(normalize=True).sort_index().cumsum()

plt.figure(figsize=(10, 4))
plt.step(ecdf.index, ecdf.values, where="post", color="blue")
plt.grid(True)
plt.title("Эмпирическая функция распределения F*(x)")
plt.xlabel("Возраст")
plt.ylabel("F*(x)")
plt.tight_layout()
plt.show()