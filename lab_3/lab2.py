import random
from scipy.stats import f


def corrected_variance(data):
    n = len(data)
    if n < 2:
        raise ValueError("В каждой выборке должно быть не менее двух наблюдений.")
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - 1)


def variance_test(x, y, alpha, two_sided):
    """Проверка H0: D1 = D2. False -> H1: D1 > D2, True -> H1: D1 != D2."""
    if not 0 < alpha < 1:
        raise ValueError("Уровень значимости должен быть между 0 и 1.")

    s1, s2 = corrected_variance(x), corrected_variance(y)
    n1, n2 = len(x), len(y)

    if s1 == 0 or s2 == 0:
        raise ValueError("F-критерий требует положительных выборочных дисперсий.")

    if s1 < s2:
        f_obs = s2 / s1
        k1, k2 = n2 - 1, n1 - 1
    else:
        f_obs = s1 / s2
        k1, k2 = n1 - 1, n2 - 1

    level = alpha / 2 if two_sided else alpha
    f_crit = f.ppf(1 - level, k1, k2)

    print(f"Число наблюдений: n1 = {n1}, n2 = {n2}")
    print(f"Исправленные дисперсии: s1^2 = {s1:.4f}, s2^2 = {s2:.4f}")
    print(f"Число степеней свободы числителя и знаменателя: k1 = {k1}, k2 = {k2}")
    print(f"Наблюдаемое значение: F_набл = {f_obs:.4f}")
    print(f"Критическое значение: F_кр = {f_crit:.4f}")

    if not two_sided and s1 < s2:
        print("ВЫВОД: F_набл < F_кр -> нет оснований отвергнуть H0. Есть основания считать, что дисперсии равны\n")
    elif f_obs < f_crit:
        print("ВЫВОД: F_набл < F_кр -> нет оснований отвергнуть H0. Есть основания считать, что дисперсии равны\n")
    elif two_sided:
        print("ВЫВОД: F_набл >= F_кр -> H0 отвергается в пользу H1: D1 != D2.\n")
    else:
        print("ВЫВОД: F_набл >= F_кр -> H0 отвергается в пользу H1: D1 > D2.\n")


alpha = 0.05
sample_size = 62


with open("../Москва_2021.txt", encoding="utf-8") as file:
    ages = [float(line.replace(",", ".").strip()) for line in file if line.strip()]


if len(ages) < sample_size:
    raise ValueError("В файле меньше наблюдений, чем размер выборки.")


x = random.sample(ages, sample_size)
y = random.sample(ages, sample_size)

print("а) Конкурирующая гипотеза H1: D1 > D2\n")
variance_test(x, y, alpha, two_sided=False)

print("б) Конкурирующая гипотеза H1: D1 != D2\n")
variance_test(x, y, alpha, two_sided=True)