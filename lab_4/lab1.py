import math
import matplotlib.pyplot as plt


discrete_series = [
    (14, 49), (15, 53), (16, 236), (17, 126), (18, 806), (19, 971),
    (20, 910), (21, 716), (22, 944), (23, 1071), (24, 810), (25, 1050),
    (26, 980), (27, 1263), (28, 1113), (29, 1340), (30, 734), (31, 1115),
    (32, 796), (33, 758), (34, 869), (35, 676), (36, 1198), (37, 522),
    (38, 1006), (39, 695), (40, 723), (41, 837), (42, 978), (43, 820),
    (44, 1032), (45, 690), (46, 677), (47, 831), (48, 1026), (49, 1060),
    (50, 150), (51, 188), (52, 193), (53, 47), (54, 26), (55, 62),
    (56, 76), (57, 136), (58, 262), (59, 74), (60, 266), (61, 226),
    (62, 139), (63, 183), (64, 189), (65, 79), (66, 188), (67, 128),
    (69, 202), (70, 26), (71, 85), (73, 17),
]


def pearson(x, y):
    n = len(x)
    x_mean, y_mean = sum(x) / n, sum(y) / n
    x_dev = [value - x_mean for value in x]
    y_dev = [value - y_mean for value in y]
    covariance = sum(dx * dy for dx, dy in zip(x_dev, y_dev)) / n
    x_std = math.sqrt(sum(dx ** 2 for dx in x_dev) / n)
    y_std = math.sqrt(sum(dy ** 2 for dy in y_dev) / n)
    if x_std == 0 or y_std == 0:
        raise ValueError("Для расчёта корреляции обе дисперсии должны быть положительными.")
    r = covariance / (x_std * y_std)
    return covariance, x_std, y_std, max(-1.0, min(1.0, r))


def student_test(r, k, alpha):
    t_obs = r * math.sqrt(k / (1 - r ** 2)) if abs(r) < 1 else math.copysign(math.inf, r)

    left, right = 0.0, math.tan(math.pi * (1 - alpha) / 2)
    sqrt_k = math.sqrt(k)
    power = k - 1
    for _ in range(50):
        middle = (left + right) / 2
        angle = math.atan(middle / sqrt_k)
        sine, cosine = math.sin(angle), math.cos(angle)
        if power % 2 == 0:
            area, total, start = angle, math.pi / 2, 2
        else:
            area, total, start = sine, 1.0, 3
        for m in range(start, power + 1, 2):
            area = (sine * cosine ** (m - 1) + (m - 1) * area) / m
            total *= (m - 1) / m
        if area / total < 1 - alpha:
            left = middle
        else:
            right = middle
    return t_obs, (left + right) / 2


x, y = zip(*discrete_series)
n = len(x)
covariance, x_std, y_std, r = pearson(x, y)
print("Лабораторная 4.1. Линейная корреляция")
print(f"Ковариация = {covariance:.4f}")
print(f"СКО X = {x_std:.4f}, СКО Y = {y_std:.4f}")
magnitude = abs(r)
print(f"r_xy = {r:.4f}, |r_xy| = {magnitude:.4f}")
if magnitude == 0:
    print("Линейная корреляция в выборке отсутствует.")
else:
    direction = "прямая" if r > 0 else "обратная"
    if magnitude <= 0.3:
        strength = "слабая"
    elif magnitude <= 0.5:
        strength = "умеренная"
    elif magnitude <= 0.7:
        strength = "заметная"
    elif magnitude < 1:
        strength = "сильная"
    else:
        strength = "линейная функциональная"
    print(f"Связь в выборке {direction}, {strength}.")

alpha = 0.05
k = n - 2
t_obs, t_crit = student_test(r, k, alpha)
print(f"\nα = {alpha}, n = {n} пар, k = {k}")
print("Критерий Стьюдента применяется в предположении двумерной нормальности.")
print("H₀: ρ_xy = 0. В генеральной совокупности линейная корреляция между возрастом и частотой равна нулю.")
print("H₁: ρ_xy ≠ 0.")
print(f"t_набл = {t_obs:.4f}, |t_набл| = {abs(t_obs):.4f}, t_кр = {t_crit:.4f}")
if abs(t_obs) < t_crit:
    print(f"\nВЫВОД: |t_набл| < t_кр. При α = {alpha:g} нет оснований отвергнуть H₀. "
          "Статистически значимая линейная связь между возрастом и частотой не установлена.")
else:
    direction = "прямой" if r > 0 else "обратной"
    print(f"\nВЫВОД: |t_набл| ≥ t_кр. При α = {alpha:g} H₀ о нулевой линейной корреляции отвергается. "
          f"Выборочный коэффициент Пирсона значимо отличается от нуля. Данные указывают на наличие "
          f"{direction} линейной связи между возрастом и частотой.")

plt.figure(figsize=(10, 4))
plt.scatter(x, y, color="blue")
plt.xticks(x, rotation=90, fontsize=8)
plt.title("Корреляционное поле")
plt.xlabel("Возраст, лет")
plt.ylabel("Частота")
plt.tight_layout()
plt.show()
