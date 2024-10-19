"""Function for join k sorted lists in 1

Tests can take a long time!!!
"""

import timeit
import random
import heapq

from typing import List
from copy import deepcopy

from progress_bar import progress_bar


def merge_k_lists_heap(lists):
    min_heap = []

    # Додаємо перші елементи з кожного списку у купу
    for i, lst in enumerate(lists):
        if lst:  # Перевіряємо, чи не пустий список
            # (значення, індекс списку, індекс елемента)
            heapq.heappush(min_heap, (lst[0], i, 0))

    merged_list = []

    while min_heap:
        value, list_index, element_index = heapq.heappop(min_heap)
        merged_list.append(value)

        # Якщо є наступний елемент у цьому списку, додаємо його в купу
        if element_index + 1 < len(lists[list_index]):
            next_value = lists[list_index][element_index + 1]
            heapq.heappush(
                min_heap, (next_value, list_index, element_index + 1))

    return merged_list


def merge_k_lists(lists: List[List[int]]) -> List[int]:
    """
    Зливає k вже відсортованих списків в один відсортований список.

    :param lists: Список відсортованих списків.
    :return: Один відсортований список.
    """
    copy_lists = deepcopy(lists)
    merged_list = []
    total_elements = sum(
        len(lst) for lst in copy_lists)  # Загальна кількість елементів

    while any(copy_lists):  # Поки хоча б один список не пустий
        # Знаходимо найменший елемент у списках
        min_value = float('inf')
        current_min = min(min(lst) for lst in copy_lists if lst)
        list_index_to_clean = [
            ind for ind, list in enumerate(copy_lists)
            if current_min in list][0]
        if current_min < min_value:
            min_value = current_min

        merged_list.append(min_value)
        # Видаляємо найменший елемент з відповідного списку
        cur_list = copy_lists[list_index_to_clean]
        cur_list.remove(current_min)

        # Оновлюємо прогрес-бар
        progress_bar(
            "Min approach progress", len(merged_list), total_elements)

    return merged_list


def merge_k_lists_iter(lists: List[List[int]]) -> List[int]:
    """
    Зливає k вже відсортованих списків в один відсортований список.

    :param lists: Список відсортованих списків.
    :return: Один відсортований список.
    """
    merged_list = []
    total_elements = sum(len(lst)
                         for lst in lists)  # Загальна кількість елементів

    # Створюємо масив для зберігання індексів
    indices = [0] * len(lists)

    while True:
        min_value = float('inf')
        min_index = -1

        # Знаходимо найменший елемент серед списків
        for i in range(len(lists)):
            # Перевіряємо, чи є ще елементи у списку
            if indices[i] < len(lists[i]):
                current_value = lists[i][indices[i]]
                if current_value < min_value:
                    min_value = current_value
                    min_index = i

        # Якщо не знайшли жодного елемента, виходимо з циклу
        if min_index == -1:
            break

        # Додаємо найменший елемент до злитого списку
        merged_list.append(min_value)
        indices[min_index] += 1  # Переходимо до наступного елемента в списку

        # Оновлюємо прогрес-бар
        progress_bar("Iter progress", len(merged_list), total_elements)

    print()  # Додаємо новий рядок після завершення прогресу
    return merged_list


def merge_k_lists_sorted(lists: List[List[int]]) -> List[int]:
    """
    Зливає k відсортованих списків в один відсортований список.

    :param lists: Список відсортованих списків.
    :return: Один відсортований список.
    """
    return sorted([item for sublist in lists for item in sublist])


# Тестові данні та генерація
lists = [
    [1, 4, 5],
    [1, 3, 4],
    [2, 6]
]


def generate_sorted_lists(num_lists: int, list_size: int) -> List[List[int]]:
    """Генерує відсортовані списки випадкових цілих чисел."""
    return [sorted([random.randint(1, 100)
                    for _ in range(list_size)]) for _ in range(num_lists)]


def generate_unsorted_lists(num_lists: int, list_size: int) -> List[List[int]]:
    """Генерує не відсортовані списки випадкових цілих чисел."""
    return [[random.randint(1, 100) for _ in range(list_size)]
            for _ in range(num_lists)]


# Тестування на різних розмірах сортованих списків
print("Тест відповідності завданню")
actual_result_heap = merge_k_lists_heap(lists)
assert actual_result_heap == [1, 1, 2, 3, 4, 4, 5, 6], \
    f'Вивід heap очікується: [1, 1, 2, 3, 4, 4, 5, 6], актуальний: "{
        actual_result_heap}"'

actual_result_sorted = merge_k_lists_sorted(lists)
assert actual_result_sorted == [1, 1, 2, 3, 4, 4, 5, 6], \
    f'Вивід sorted очікується: [1, 1, 2, 3, 4, 4, 5, 6], актуальний: "{
        actual_result_sorted}"'

actual_result_min = merge_k_lists(lists)
assert actual_result_min == [1, 1, 2, 3, 4, 4, 5, 6], \
    f'Вивід min очікується: [1, 1, 2, 3, 4, 4, 5, 6], актуальний: "{
        actual_result_min}"'

actual_result_iter = merge_k_lists_iter(lists)
assert actual_result_iter == [1, 1, 2, 3, 4, 4, 5, 6], \
    f'Вивід iter очікується: [1, 1, 2, 3, 4, 4, 5, 6], актуальний: "{
        actual_result_iter}"'

print("\nВідсортований список купою:", actual_result_sorted)
print("Відсортований список sorted:", actual_result_sorted)
print("Відсортований список min:", actual_result_min, "\n")
print("Відсортований список iter:", actual_result_iter, "\n")


sizes = [
    (1, 10), (10, 10), (10, 100), (100, 10),
    (100, 100), (100, 1000)
]

print("Вивід ефективності з порівнянням відсортованих списків")
counter = 0
len_sizes = len(sizes)
for num_lists, list_size in sizes:
    sorted_lists = generate_sorted_lists(num_lists, list_size)

    # Час для злиття через купу
    time_heapq = timeit.timeit(
        lambda: merge_k_lists_heap(sorted_lists), number=100
    )
    print("\nЗлиття купою завершено")
    # Час для злиття через нативний метод
    time_sorted = timeit.timeit(
        lambda: merge_k_lists_sorted(sorted_lists), number=100
    )
    print("\nЗлиття sorted завершено")
    if list_size < 1000:
        # Час для злиття через min метод
        time_min = timeit.timeit(
            lambda: merge_k_lists(sorted_lists), number=100
        )
        print("\nЗлиття min завершено")

        # Час для злиття через ітеративний метод
        time_iter = timeit.timeit(
            lambda: merge_k_lists_iter(sorted_lists), number=100
        )
        print("\nЗлиття iter завершено")

    print(f"Розмір: {num_lists} сортованих списків по {
        list_size} елементів:")
    print(f"\nЗлиття з купою завершено за: {time_heapq:.6f} секунд")
    print(f"\nЗлиття з sorted завершено за: {time_sorted:.6f} секунд")
    if list_size < 1000:
        print(f"\nЗлиття з min завершено за: {time_min:.6f} секунд")
        print(f"\nЗлиття з iter завершено за: {time_iter:.6f} секунд")
    else:
        print("Methods which not effective for large data are skipped")
    counter += 1
    progress_bar("Compare sorted analisys bar", counter, len_sizes)
print("Сортування відсортованих списків завершене")

# Тестування на різних розмірах не сортованих списків

print("Вивід ефективності з порівнянням не відсортованих списків")
counter = 0
len_sizes = len(sizes)
for num_lists, list_size in sizes:
    unsorted_lists = generate_unsorted_lists(num_lists, list_size)

    # Час для злиття через купу
    time_heapq = timeit.timeit(
        lambda: merge_k_lists_heap(unsorted_lists), number=100
    )
    print("\nЗлиття купою завершено")
    # Час для злиття через нативний метод
    time_sorted = timeit.timeit(
        lambda: merge_k_lists_sorted(unsorted_lists), number=100
    )
    print("\nЗлиття sorted завершено")
    if list_size < 1000:
        # Час для злиття через min метод
        time_min = timeit.timeit(
            lambda: merge_k_lists(unsorted_lists), number=100
        )
        print("\nЗлиття min завершено")
        # Час для злиття через ітеративний метод
        time_iter = timeit.timeit(
            lambda: merge_k_lists_iter(unsorted_lists), number=100
        )
        print("\nЗлиття iter завершено")

    print(f"Розмір: {num_lists} не сортованих списків по {
        list_size} елементів:")
    print(f"\nЗлиття з купою завершено за: {time_heapq:.6f} секунд")
    print(f"\nЗлиття з sorted завершено за: {time_sorted:.6f} секунд")
    if list_size < 1000:
        print(f"\nЗлиття з min завершено за: {time_min:.6f} секунд")
        print(f"\nЗлиття з iter завершено за: {time_iter:.6f} секунд")
    else:
        print("Methods which not effective for large data are skipped")
    counter += 1
    progress_bar("Compare unsorted analisys bar", counter, len_sizes)
print("Сортування не відсортованих списків завершене")


"""
Висновок зрівняння:
Злиття за допомогою мінімальної купи доволі ефективне
й справляється краще ніж ітеративні підходи,
але поступається нативному сортуванню.
На невідсортованих даних сортування з купою
себе показло з кращою динамікою ніж нативне сортування
так як час сортування зменшився у підходу з купами
й збільшився у нативного сортування.
Можливо на дуже великих даних вони можуть навіть
зрівнятися по часу виконання.


Результати:
Розмір: 10 сортованих списків по 10 елементів:

Злиття з купою завершено за: 0.004856 секунд
Злиття з sorted завершено за: 0.000743 секунд
Злиття з min завершено за: 0.715909 секунд
Злиття з iter завершено за: 0.681810 секунд

Розмір: 10 сортованих списків по 100 елементів:

Злиття з купою завершено за: 0.045936 секунд
Злиття з sorted завершено за: 0.006021 секунд
Злиття з min завершено за: 8.577541 секунд
Злиття з iter завершено за: 7.060839 секунд

Розмір: 100 сортованих списків по 10 елементів:

Злиття з купою завершено за: 0.065956 секунд
Злиття з sorted завершено за: 0.012091 секунд
Злиття з min завершено за: 10.913945 секунд
Злиття з iter завершено за: 8.917049 секунд

Розмір: 100 сортованих списків по 100 елементів:

Злиття з купою завершено за: 0.627661 секунд
Злиття з sorted завершено за: 0.063053 секунд
Злиття з min завершено за: 242.605401 секунд
Злиття з iter завершено за: 91.961853 секунд

Розмір: 100 сортованих списків по 1000 елементів:

Злиття з купою завершено за: 6.782427 секунд
Злиття з sorted завершено за: 0.489627 секунд
Not effective methods for large data was skipped
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Розмір: 1 не сортованих списків по 10 елементів:

Злиття з купою завершено за: 0.000308 секунд
Злиття з sorted завершено за: 0.000078 секунд
Злиття з min завершено за: 0.074932 секунд
Злиття з iter завершено за: 0.096179 секунд

Розмір: 10 не сортованих списків по 10 елементів:

Злиття з купою завершено за: 0.004686 секунд
Злиття з sorted завершено за: 0.000880 секунд
Злиття з min завершено за: 0.800115 секунд
Злиття з iter завершено за: 0.755646 секунд

Розмір: 10 не сортованих списків по 100 елементів:

Злиття з купою завершено за: 0.051162 секунд
Злиття з sorted завершено за: 0.011791 секунд
Злиття з min завершено за: 9.697559 секунд
Злиття з iter завершено за: 8.098093 секунд

Розмір: 100 не сортованих списків по 10 елементів:

Злиття з купою завершено за: 0.073568 секунд
Злиття з sorted завершено за: 0.012512 секунд
Злиття з min завершено за: 12.445185 секунд
Злиття з iter завершено за: 9.590019 секунд

Розмір: 100 не сортованих списків по 100 елементів:

Злиття з купою завершено за: 0.596038 секунд
Злиття з sorted завершено за: 0.125378 секунд
Злиття з min завершено за: 235.438445 секунд
Злиття з iter завершено за: 89.360423 секунд

Розмір: 100 не сортованих списків по 1000 елементів:

Злиття з купою завершено за: 6.264036 секунд
Злиття з sorted завершено за: 1.356290 секунд
Methods which not effective for large data was skipped
"""
