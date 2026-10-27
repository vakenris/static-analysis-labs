import math
import pandas as pd
import matplotlib.pyplot as plt

ages_series = pd.read_csv("../Москва_2021.txt", header=None, names=["age"])["age"]
ages_list = ages_series.tolist()

freq_dict = {}
for age in ages_list:
    freq_dict[age] = freq_dict.get(age, 0) + 1

sorted_ages = sorted(freq_dict.keys())
discrete_series = pd.Series({age: freq_dict[age] for age in sorted_ages})

qw_int = 7
min_age = min(ages_list)
max_age = max(ages_list)
step = math.ceil((max_age - min_age) / qw_int)

bins = [min_age + i * step for i in range(8)]
midpoints = [(bins[i] + bins[i + 1]) / 2 for i in range(qw_int)]

counts = [0] * qw_int
for age in ages_list:
    idx = int((age - min_age) / step)
    if idx >= qw_int:
        idx = 6
    counts[idx] += 1

interval_labels = []
for i in range(qw_int):
    if i == qw_int - 1:
        interval_labels.append(f"[{bins[i]} - {bins[i + 1]}]")
    else:
        interval_labels.append(f"[{bins[i]} - {bins[i + 1]})")
# interval_labels = [f"[{bins[i]} - {bins[i + 1]})" for i in range(qw_int)]
interval_series = pd.Series(counts, index=interval_labels, name="count")


def get_discrete_stats(data_list):
    n = len(data_list)
    mean = sum(data_list) / n

    var = sum((x - mean) ** 2 for x in data_list) / n
    std = math.sqrt(var)

    counts_map = {}
    for item in data_list:
        counts_map[item] = counts_map.get(item, 0) + 1

    max_freq = max(counts_map.values())
    mode_val = min([k for k, v in counts_map.items() if v == max_freq])

    sorted_data = sorted(data_list)
    mid = n // 2
    if n % 2 != 0:
        median_val = sorted_data[mid]
    else:
        median_val = (sorted_data[mid - 1] + sorted_data[mid]) / 2

    min_val = min(data_list)
    max_val = max(data_list)

    return {
        "Среднее": mean,
        "Дисперсия": var,
        "СКО": std,
        "Коэффициент вариации": (std / mean) * 100,
        "Мода": mode_val,
        "Частота моды": max_freq,
        "Медиана": median_val,
        "Минимум": min_val,
        "Максимум": max_val,
        "Размах": max_val - min_val
    }


def get_interval_stats(counts_list, bins_list, midpoints_list, step_val):
    total = sum(counts_list)

    mean = sum(m * c for m, c in zip(midpoints_list, counts_list)) / total

    var = sum(c * (m - mean) ** 2 for m, c in zip(midpoints_list, counts_list)) / total
    std = math.sqrt(var)

    max_freq = max(counts_list)
    modal_idx = counts_list.index(max_freq)
    prev_freq = counts_list[modal_idx - 1] if modal_idx > 0 else 0
    next_freq = counts_list[modal_idx + 1] if modal_idx < len(counts_list) - 1 else 0

    mode_denom = (max_freq - prev_freq) + (max_freq - next_freq)
    if mode_denom != 0:
        mode_val = bins_list[modal_idx] + step_val * ((max_freq - prev_freq) / mode_denom)
    else:
        mode_val = midpoints_list[modal_idx]

    cum_sum = 0
    med_idx = 0
    prev_cum_sum = 0
    for i, c in enumerate(counts_list):
        cum_sum += c
        if cum_sum >= total / 2:
            med_idx = i
            prev_cum_sum = cum_sum - c
            break

    median_val = bins_list[med_idx] + step_val * ((total / 2 - prev_cum_sum) / counts_list[med_idx])

    min_val = bins_list[0]
    max_val = bins_list[-1]

    return {
        "Среднее": mean,
        "Дисперсия": var,
        "СКО": std,
        "Коэффициент вариации": (std / mean) * 100,
        "Модальный интервал": mode_val,
        "Частота модального интервала": max_freq,
        "Медиана": median_val,
        "Минимум": min_val,
        "Максимум": max_val,
        "Размах": max_val - min_val
    }


print("Дискретный ряд распределения")
print(discrete_series)

print("\nСтатистика дискретного ряда")
for key, val in get_discrete_stats(ages_list).items():
    if isinstance(val, float):
        print(f"{key}: {val:.4f}")
    else:
        print(f"{key}: {val}")

print("\nИнтервальный ряд распределения")
print(interval_series)

print("\nСтатистика интервального ряда")
for key, val in get_interval_stats(counts, bins, midpoints, step).items():
    if isinstance(val, float):
        print(f"{key}: {val:.4f}")
    else:
        print(f"{key}: {val}")

discrete_series.plot(
    kind="line", marker="o", figsize=(10, 4), color="blue", grid=True,
    title="Полигон частот (дискретный ряд)", xlabel="Возраст", ylabel="Частота"
)
plt.show()

ages_series.plot(
    kind="hist", bins=bins, figsize=(10, 4), color="orange", edgecolor="black", grid=True,
    title="Гистограмма частот (интервальный ряд)", xlabel="Возраст", ylabel="Частота"
)
plt.xticks(bins)
plt.show()