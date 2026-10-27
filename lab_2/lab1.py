import math
import random
import matplotlib.pyplot as plt

with open("../Москва_2021.txt", encoding="utf-8") as file:
    population = [float(line) for line in file if line.strip()]

N = len(population)
general_mean = sum(population) / N
general_variance = sum((x - general_mean) ** 2 for x in population) / N
general_sigma = math.sqrt(general_variance)

gamma = 0.95
t = 1.96
delta = 3

n = math.ceil(t ** 2 * general_sigma ** 2 / delta ** 2)

samples_count = 36

samples = [random.choices(population, k=n) for _ in range(samples_count)]
sample_means = [sum(sample) / n for sample in samples]

print(f"Объем генеральной совокупности N = {N}")
print(f"Генеральная средняя = {general_mean:.3f}")
print(f"Генеральное СКО = {general_sigma:.3f}")
print(f"Объем выборки n = {n}")
print("Выборочные средние:")
for i, mean in enumerate(sample_means, 1):
    print(f"{i:2}: {mean:.3f}")

left = math.floor(min(sample_means))
right = math.ceil(max(sample_means))
h = 1
borders = list(range(left, right + h, h))

frequencies = []
for i in range(len(borders) - 1):
    a, b = borders[i], borders[i + 1]
    if b == right:
        count = sum(1 for m in sample_means if a <= m <= b)
    else:
        count = sum(1 for m in sample_means if a <= m < b)
    frequencies.append(count)

relative_frequencies = [f / samples_count for f in frequencies]

print("\nИнтервальный ряд:")
print("Интервал    n_i    w_i")
for i in range(len(frequencies)):
    closing_bracket = "]" if i == len(frequencies) - 1 else ")"
    print(
        f"[{borders[i]}; {borders[i + 1]}{closing_bracket}   {frequencies[i]:3}   {relative_frequencies[i]:.3f}"
    )
print(f"Сумма w_i = {sum(relative_frequencies):.3f}")

plt.bar(borders[:-1], relative_frequencies, width=h, align="edge", edgecolor="black")
plt.xticks(borders)
plt.xlim(left - 0.5, right + 0.5)
plt.xlabel("Выборочная средняя возраста, лет")
plt.ylabel("Относительная частота w_i")
plt.title("Гистограмма относительных частот выборочных средних")
plt.show()