import math
import random
from scipy.stats import chi2


def pearson_test(bounds, freqs, alpha=0.05, is_first_task=False, ages_data=None):
    s = len(freqs)
    n = sum(freqs)

    if is_first_task and ages_data is not None:
        mean_gen = sum(ages_data) / n
        sigma_gen = math.sqrt(sum((x - mean_gen) ** 2 for x in ages_data) / n)
        print(f"Генеральное СКО = {sigma_gen:.4f}")

    mids = [(bounds[i] + bounds[i + 1]) / 2 for i in range(s)]
    mean = sum(m * f for m, f in zip(mids, freqs)) / n
    sigma = math.sqrt(sum(f * (m - mean) ** 2 for m, f in zip(mids, freqs)) / n)

    z = [(b - mean) / sigma for b in bounds]
    z[0], z[-1] = -math.inf, math.inf

    print(f"n = {n}, x_ср = {mean:.4f}, sigma (интервальное) = {sigma:.4f}, alpha = {alpha}\n")

    print(
        f"{'i':>2} | {'x_i':>7} {'x_i+1':>7} | {'z_i':>7} {'z_i+1':>7} | {'Ф(z_i)':>8} {'Ф(z_i+1)':>9} | {'p_i':>7} | {'n_i':>5} | {'n_i`':>7}")
    print("-" * 80)

    chi2_val = 0.0
    control = 0.0
    for i in range(s):
        f1 = 0.5 * math.erf(z[i] / math.sqrt(2))
        f2 = 0.5 * math.erf(z[i + 1] / math.sqrt(2))
        p = f2 - f1
        n_t = n * p
        if n_t == 0:
            n_t = 1e-5

        chi2_val += (freqs[i] - n_t) ** 2 / n_t
        control += (freqs[i] ** 2) / n_t

        z_i_str = f"{z[i]:.2f}" if z[i] != -math.inf else "-inf"
        z_ip1_str = f"{z[i + 1]:.2f}" if z[i + 1] != math.inf else "+inf"

        print(f"{i + 1:>2} | {bounds[i]:>7.2f} {bounds[i + 1]:>7.2f} | {z_i_str:>7} {z_ip1_str:>7} | {f1:>8.3f} {f2:>9.3f} | {p:>7.3f} | {freqs[i]:>5} | {n_t:>7.2f}")

    r = 2
    k = s - 1 - r

    chi2_crit = chi2.ppf(1 - alpha, k)

    print("-" * 80)
    print(f"Число степеней свободы: k = {s} - 1 - {r} = {k}")
    print(f"Контроль: sum(n_i^2 / n_i`) - n = {control - n:.4f}")
    print(f"chi2_набл = {chi2_val:.4f}")
    print(f"chi2_кр (alpha={alpha}; k={k}) = {chi2_crit:.4f}")
    print()

    if chi2_val < chi2_crit:
        print("ВЫВОД: chi2_набл < chi2_кр: нет оснований отвергнуть H0 (данные согласуются с нормальным распределением).\n")
    else:
        print("ВЫВОД: chi2_набл > chi2_кр: H0 отвергается (распределение не нормальное).\n")


alpha = 0.05

with open("../Москва_2021.txt", encoding="utf-8") as file:
    population = [float(line.replace(",", ".").strip()) for line in file if line.strip()]

bounds1 = [14, 23, 32, 41, 50, 59, 68, 77]
freqs1 = [4811, 9476, 7243, 7951, 1140, 1472, 330]

print("Задание 1: возраст")
raw_ages_flat = []
for b_start, b_end, f_val in zip(bounds1[:-1], bounds1[1:], freqs1):
    mid = (b_start + b_end) / 2
    raw_ages_flat.extend([mid] * f_val)

pearson_test(bounds1, freqs1, alpha, is_first_task=True, ages_data=raw_ages_flat)

N = len(population)
general_mean = sum(population) / N
general_sigma = math.sqrt(sum((x - general_mean) ** 2 for x in population) / N)

t_laplace = 1.96
delta = 3.0
n = math.ceil((t_laplace ** 2 * general_sigma ** 2) / (delta ** 2))

samples_count = 36
samples = [random.choices(population, k=n) for _ in range(samples_count)]
sample_means = [sum(sample) / n for sample in samples]

left = math.floor(min(sample_means))
right = math.ceil(max(sample_means))
h = 1
bounds2 = list(range(left, right + h, h))

freqs2 = []
for i in range(len(bounds2) - 1):
    a, b = bounds2[i], bounds2[i + 1]
    if b == right:
        count = sum(1 for m in sample_means if a <= m <= b)
    else:
        count = sum(1 for m in sample_means if a <= m < b)
    freqs2.append(count)

print("Задание 2: средний возраст")
pearson_test(bounds2, freqs2, alpha, is_first_task=False)