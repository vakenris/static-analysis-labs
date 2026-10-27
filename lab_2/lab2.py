import math
import random
import matplotlib.pyplot as plt

def get_student_quantile(k):
    student_table = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447,
        7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179,
        13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101,
        19: 2.093, 20: 2.086, 25: 2.060, 30: 2.042, 40: 2.021, 50: 2.009,
        60: 2.000, 80: 1.990, 100: 1.984, 120: 1.980
    }
    if k in student_table:
        return student_table[k]
    if k > 120:
        return 1.960
    if k < 1:
        return student_table[1]
    keys = sorted(student_table.keys())
    k1 = max(key for key in keys if key < k)
    k2 = min(key for key in keys if key > k)
    t1, t2 = student_table[k1], student_table[k2]
    return round(t1 + (t2 - t1) * (k - k1) / (k2 - k1), 4)

with open("../Москва_2021.txt", encoding="utf-8") as file:
    population = [float(line) for line in file if line.strip()]

N = len(population)
general_mean = sum(population) / N
general_sigma = math.sqrt(sum((x - general_mean) ** 2 for x in population) / N)

gamma = 0.95
t_laplace = 1.96
delta = 3.0
n = math.ceil((t_laplace ** 2 * general_sigma ** 2) / (delta ** 2))

samples_count = 36
samples = [random.choices(population, k=n) for _ in range(samples_count)]
sample_means = [sum(sample) / n for sample in samples]

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
midpoints = [(borders[i] + borders[i + 1]) / 2 for i in range(len(borders) - 1)]

a_estimate = sum(x * w for x, w in zip(midpoints, relative_frequencies))
d_estimate = sum((x - a_estimate) ** 2 * w for x, w in zip(midpoints, relative_frequencies))
sigma_estimate = math.sqrt(d_estimate)

print("Задание 1. Метод моментов")
print(f"a = {a_estimate:.3f}")
print(f"D = {d_estimate:.3f}")
print(f"sigma = {sigma_estimate:.3f}")

def gauss(x, a, sigma):
    return math.exp(-(x - a) ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))

print("\nx      f(x)")
for x in borders:
    print(f"{x:<6} {gauss(x, a_estimate, sigma_estimate):.4f}")

densities = [w / h for w in relative_frequencies]
steps = 200
xs = [left - 1 + i * (right - left + 2) / steps for i in range(steps + 1)]
ys = [gauss(x, a_estimate, sigma_estimate) for x in xs]

plt.bar(borders[:-1], densities, width=h, align="edge", edgecolor="black", alpha=0.6, label="Гистограмма")
plt.plot(xs, ys, color="red", label="Кривая Гаусса")
plt.xticks(borders)
plt.xlim(left - 0.5, right + 0.5)
plt.xlabel("Средний возраст, лет")
plt.ylabel("w_i / h,  f(x)")
plt.title("Выравнивание статистического ряда нормальным законом")
plt.legend()
plt.show()

sample = samples[0]
sample_size = len(sample)
k = sample_size - 1

x_mean = sum(sample) / sample_size
s = math.sqrt(sum((x - x_mean) ** 2 for x in sample) / k)

t_gamma = get_student_quantile(k)
accuracy = t_gamma * s / math.sqrt(sample_size)

print("\nЗадание 2. Доверительный интервал")
print(f"Объем выборки n = {sample_size}")
print(f"Число степеней свободы k = {k}")
print(f"Точечная оценка x̄ = {x_mean:.3f}")
print(f"Исправленное СКО s = {s:.3f}")
print(f"Квантиль Стьюдента t = {t_gamma:.4f}")
print(f"Точность delta = {accuracy:.3f}")
print(f"Интервальная оценка: {x_mean - accuracy:.3f} < a < {x_mean + accuracy:.3f}")