import math


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

interval_series = [
    (14, 23, 4811), (23, 32, 9476), (32, 41, 7243), (41, 50, 7951),
    (50, 59, 1140), (59, 68, 1472), (68, 77, 330),
]


def age_statistics(series):
    total = sum(frequency for _, frequency in series)
    mean = sum(age * frequency for age, frequency in series) / total
    variance = sum((age - mean) ** 2 * frequency for age, frequency in series) / total
    return total, mean, variance


def spearman(x, y):
    rank_columns = []
    for values in (x, y):
        counts = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1

        ranks = {}
        first = 1
        for value, count in sorted(counts.items()):
            ranks[value] = first + (count - 1) / 2
            first += count
        rank_columns.append([ranks[value] for value in values])

    rank_x, rank_y = rank_columns
    n = len(x)
    sum_d2 = sum((rx - ry) ** 2 for rx, ry in zip(rank_x, rank_y))
    return 1 - 6 * sum_d2 / (n * (n ** 2 - 1))


def grouped_variances(series, intervals):
    total, mean, total_var = age_statistics(series)
    within_sum = between_sum = 0.0
    print(f"N = {total}, средний возраст = {mean:.4f}")
    print("Интервал     N_j     x̄_j     D_j")
    for i, (left, right, count) in enumerate(intervals):
        is_last = i == len(intervals) - 1
        closing = "]" if is_last else ")"
        label = f"[{left}; {right}{closing}"
        group = [
            (age, frequency) for age, frequency in series
            if left <= age < right or (is_last and age == right)
        ]
        group_count, group_mean, group_var = age_statistics(group)
        if group_count != count:
            raise ValueError(f"Частоты рядов не совпадают в интервале {label}.")
        within_sum += group_var * count
        between_sum += (group_mean - mean) ** 2 * count
        print(f"{label:<12} {count:>4} {group_mean:>8.4f} {group_var:>8.4f}")
    return within_sum / total, between_sum / total, total_var


print("Лабораторная 4.2. Нелинейная зависимость")
within_var, between_var, total_var = grouped_variances(discrete_series, interval_series)
variance_sum = within_var + between_var
print(f"\nD_внгр = {within_var:.4f}")
print(f"D_межгр = {between_var:.4f}")
print(f"D_общ = {total_var:.4f}, D_внгр + D_межгр = {variance_sum:.4f}")
if math.isclose(total_var, variance_sum):
    variance_result = "Формула общей дисперсии выполняется."
else:
    variance_result = "Формула общей дисперсии не выполняется."

between_share = between_var / total_var
eta = math.sqrt(between_share)
x, y = zip(*discrete_series)
rank_correlation = spearman(x, y)
print(f"Корреляционное отношение η = {eta:.4f}")
print(f"Коэффициент Спирмена R = {rank_correlation:.4f}")

if rank_correlation < 0:
    rank_result = "По Спирмену связь обратная. С ростом возраста частота в целом снижается."
elif rank_correlation > 0:
    rank_result = "По Спирмену связь прямая. С ростом возраста частота в целом увеличивается."
else:
    rank_result = "Коэффициент Спирмена равен нулю. Монотонная связь в ряду не выявлена."

print(f"\nВЫВОД: {variance_result} На различия между возрастными интервалами приходится "
      f"{between_share:.1%} общей дисперсии возраста. {rank_result}")
