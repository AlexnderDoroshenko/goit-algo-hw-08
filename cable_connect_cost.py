import heapq
from typing import List

from progress_bar import progress_bar


def min_cost_to_connect_cables(cables: List[int]) -> int:
    """
    Обчислює мінімальні витрати на з'єднання мережевих кабелів.

    :param cables: Список довжин кабелів.
    :return: Загальні витрати на з'єднання кабелів.
    """
    if len(cables) <= 1:
        return 0  # Витрати на з'єднання одного або менше кабеля

    heapq.heapify(cables)
    total_cost = 0
    while len(cables) > 1:
        first = heapq.heappop(cables)  # Перша найменша довжина кабелю
        second = heapq.heappop(cables)  # Друга найменша довжина кабелю
        cost = first + second  # Витрати на з'єднання двох кабелів
        total_cost += cost  # Додамо до Загальних витрат суму витрат на з'єднання
        heapq.heappush(cables, cost)

    return total_cost


# Тестування функції min_cost_to_connect_cables
cost_dict = {
    58: [8, 4, 6, 12],  # Для [8, 4, 6, 12]
    9: [1, 2, 3],   # Для [1, 2, 3]
    77: [5, 9, 10, 15],  # Для [5, 9, 10, 15]
    900: [100, 200, 300],  # Для [100, 200, 300]
    0: [30],   # Для [30]
    1500: [500, 300, 200],  # Для [500, 300, 200]
    13000: [7000, 1000, 2000],  # Для [7000, 1000, 2000]
    31999: [9999, 5000, 3000, 1000],  # Для [9999, 5000, 3000, 1000]
}

# Тестування
total_tests = len(cost_dict)
for i, (expected_cost, cables) in enumerate(cost_dict.items()):
    total_cost = min_cost_to_connect_cables(cables)
    print(f"\nДовжини кабелів: {cables} -> Загальні витрати: {total_cost}")

    # Простий асерт для перевірки результату
    assert total_cost == expected_cost, f"Помилка: очікувалося {
        expected_cost}, отримано {total_cost}"

    progress_bar("Cost cable connect bar", i + 1, total_tests)

print("\nТестування Успішне!")
