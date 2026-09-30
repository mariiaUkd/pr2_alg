import random

def generate_matrix(m, n, low, high):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(m)]

def print_matrix(matrix):
    for row in matrix:
        print(*row, sep="\t")

def subtract_row_mean(matrix):
    return [[round(x - sum(row)/len(row), 2) for x in row] for row in matrix]

def cyclic_shift(matrix, k):
    n, m = len(matrix[0]), len(matrix)
    k_col, k_row = k % n, k % m
    shifted = [row[-k_col:] + row[:-k_col] for row in matrix]
    return shifted[k_row:] + shifted[:k_row]

def remove_rows_cols_with_max(matrix):
    max_val = max(x for row in matrix for x in row)
    rows = {i for i, row in enumerate(matrix) if max_val in row}
    cols = {j for j in range(len(matrix[0])) if any(r[j] == max_val for r in matrix)}
    return [[v for j, v in enumerate(row) if j not in cols]
            for i, row in enumerate(matrix) if i not in rows], max_val

def rotate_90_clockwise_inplace(m):
    n = len(m)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            off = i - first
            top = m[first][i]
            m[first][i] = m[last - off][first]
            m[last - off][first] = m[last][last - off]
            m[last][last - off] = m[i][last]
            m[i][last] = top
    return m


GROUPS = ["Гр.1", "Гр.2", "Гр.3"]
DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт"]
SUBJECTS = ["Матем.", "Фізика", "Програм.", "Англ.", "БД", "Алгоритми"]
FREE = "Вікно"

def generate_schedule():
    return [[[random.choice(SUBJECTS + [FREE]) for _ in range(4)]
             for _ in DAYS] for _ in GROUPS]

def busiest_day(schedule, g):
    loads = [sum(p != FREE for p in day) for day in schedule[g]]
    i = loads.index(max(loads))
    return DAYS[i], loads[i]

def day_with_windows(schedule, g):
    result = []
    for i, day in enumerate(schedule[g]):
        busy = [j for j, p in enumerate(day) if p != FREE]
        if busy and any(day[j] == FREE for j in range(busy[0], busy[-1] + 1)):
            result.append(DAYS[i])
    return result

def find_stream_classes(schedule):
    streams = []
    for d in range(len(DAYS)):
        for p in range(4):
            seen = {}
            for g, group in enumerate(schedule):
                subj = group[d][p]
                if subj != FREE:
                    seen.setdefault(subj, []).append(GROUPS[g])
            streams += [(DAYS[d], p + 1, s, gs) for s, gs in seen.items() if len(gs) > 1]
    return streams


if __name__ == "__main__":
    random.seed(1)
    m = generate_matrix(4, 4, 0, 10)
    print_matrix(m)
    print("\nСереднє віднято:"); print_matrix(subtract_row_mean(m))
    print("\nЗсув k=1:"); print_matrix(cyclic_shift(m, 1))
    cleaned, mx = remove_rows_cols_with_max(m)
    print(f"\nMax={mx}, після видалення:"); print_matrix(cleaned)
    print("\nОбертання 90°:"); print_matrix(rotate_90_clockwise_inplace(m))

    sch = generate_schedule()
    print("\nНайзавантаженіший день (Гр.1):", busiest_day(sch, 0))
    print("Дні з вікнами (Гр.1):", day_with_windows(sch, 0))
    print("Потокові заняття:", find_stream_classes(sch))