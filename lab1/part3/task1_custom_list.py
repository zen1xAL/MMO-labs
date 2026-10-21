"""
Лабораторная работа №1. Часть 3.
Вариант 7. Задание 1.

Условие:
Создать класс List (список), в котором реализовать методы для работы со
списком (не менее 5).
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


class CustomList:
    """
    Класс для работы со списком (инкапсуляция и методы обработки).
    """

    def __init__(self, initial: Optional[List[Any]] = None) -> None:
        self._items: List[Any] = list(initial) \
            if initial is not None else []

    # 1. Добавление элемента
    def append(self, item: Any) -> None:
        self._items.append(item)

    # 2. Удаление по значению
    def remove(self, value: Any) -> bool:
        try:
            self._items.remove(value)
            return True
        except ValueError:
            return False

    # 3. Разворот списка
    def reverse(self) -> None:
        self._items.reverse()

    # 4. Сортировка
    def sort(self, reverse: bool = False) -> None:
        self._items.sort(reverse=reverse)

    # 5. Поиск min и max
    def find_min_max(self) -> Tuple[Any, Any]:
        if not self._items:
            raise ValueError("Список пуст.")
        return min(self._items), max(self._items)

    # 6. Уникальные элементы
    def get_unique(self) -> List[Any]:
        return list(dict.fromkeys(self._items))

    # 7. Фильтрация
    def filter_by(self, predicate: Callable[[Any], bool]) -> "CustomList":
        return CustomList([x for x in self._items if predicate(x)])

    # 8. Частоты элементов
    def count_frequency(self) -> Dict[Any, int]:
        freq: Dict[Any, int] = {}
        for x in self._items:
            freq[x] = freq.get(x, 0) + 1
        return freq

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, idx: int) -> Any:
        return self._items[idx]

    def __str__(self) -> str:
        return f"CustomList({self._items})"


def main() -> None:
    print("=" * 60)
    print("Задание 3.1: Класс CustomList (методы работы со списком)")
    print("=" * 60)

    clist = CustomList([25, 12, 88, 7, 45, 12, 99, 3, 45, 7, 100, -5])
    print(f"Инициализация: {clist}")

    clist.append(500)
    print(f"После append(500): {clist}")

    clist.remove(12)
    print(f"После remove(12):  {clist}")

    clist.reverse()
    print(f"После reverse():   {clist}")

    clist.sort(reverse=False)
    print(f"Сортировка (asc):  {clist}")
    clist.sort(reverse=True)
    print(f"Сортировка (desc): {clist}")

    mi, ma = clist.find_min_max()
    print(f"Min: {mi}, Max: {ma}")
    print(f"Уникальные: {clist.get_unique()}")
    print(f"Фильтр (>30): {clist.filter_by(lambda x: x > 30)}")
    print(f"Частоты: {clist.count_frequency()}")


if __name__ == "__main__":
    main()
