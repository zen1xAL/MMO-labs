"""
Лабораторная работа №1. Часть 3.
Вариант 7. Задание 2.

Условие:
Создать классы «Транспортное средство», «Самолет», «Поезд», «Автомобиль».
Определить время и стоимость перевозки для указанных городов и расстояний.
Вывести данные о наиболее быстрой и экономичной поездке.
Предусмотреть метод записи информации в файл.
"""

from abc import ABC
from typing import Any, Dict, List


class Transport(ABC):
    def __init__(
        self, name: str, speed: float, rate: float, fee: float, prep: float
    ) -> None:
        self.name = name
        self.speed = speed
        self.rate = rate
        self.fee = fee
        self.prep = prep

    def calc_time(self, dist: float) -> float:
        return self.prep + (dist / self.speed) if dist > 0 else 0.0

    def calc_cost(self, dist: float) -> float:
        return self.fee + (self.rate * dist) if dist > 0 else 0.0

    def trip_info(
        self, orig: str, dest: str, dist: float
    ) -> Dict[str, Any]:
        return {
            "name": self.name,
            "orig": orig,
            "dest": dest,
            "dist": dist,
            "time": self.calc_time(dist),
            "cost": self.calc_cost(dist),
        }


class Airplane(Transport):
    def __init__(self) -> None:
        super().__init__("Самолёт", 800.0, 0.22, 45.0, 2.0)


class Train(Transport):
    def __init__(self) -> None:
        super().__init__("Поезд", 90.0, 0.065, 5.0, 0.5)


class Car(Transport):
    def __init__(self) -> None:
        super().__init__("Автомобиль", 100.0, 0.16, 0.0, 0.15)


def compare_trips(
    orig: str, dest: str, dist: float
) -> List[Dict[str, Any]]:
    transports = [Airplane(), Train(), Car()]
    return [t.trip_info(orig, dest, dist) for t in transports]


def save_to_file(filepath: str, all_trips_data: List[Any]) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("ОТЧЕТ ПО СРАВНЕНИЮ ТРАНСПОРТА\n")
        f.write("=" * 45 + "\n")
        for item in all_trips_data:
            f.write(f"\n{item['orig']} - {item['dest']} ({item['dist']:.0f} км)\n")
            for t in item["trips"]:
                f.write(f"  {t['name']:<9}: {t['time']:>5.2f}ч {t['cost']:>6.2f}р\n")
            f.write(f"  Быстрейший:  {item['fastest']['name']}\n")
            f.write(f"  Экономичный: {item['cheapest']['name']}\n")


def main() -> None:
    print("=" * 60)
    print("Задание 3.2: Иерархия транспортных средств")
    print("=" * 60)

    routes = [
        ("Минск", "Брест", 350.0),
        ("Минск", "Москва", 720.0),
        ("Минск", "Санкт-Петербург", 790.0),
    ]

    all_data = []
    for orig, dst, dist in routes:
        trips = compare_trips(orig, dst, dist)
        fastest = min(trips, key=lambda x: x["time"])
        cheapest = min(trips, key=lambda x: x["cost"])
        all_data.append({"orig": orig, "dest": dst, "dist": dist,
                         "trips": trips,
             "fastest": fastest, "cheapest": cheapest})

        print(f"\nМаршрут: {orig} -> {dst} ({dist} км)")
        for t in trips:
            print(f"  {t['name']:<10}: {t['time']:>5.2f} ч, {t['cost']:>6.2f} руб.")
        print(f"  • Быстрее: {fastest['name']} ({fastest['time']:.2f} ч)")
        print(f"  • Дешевле: {cheapest['name']} ({cheapest['cost']:.2f} руб.)")

    save_to_file("d:/MMO/part3/trips_report.txt", all_data)
    print("\nОтчет сохранен в: d:/MMO/part3/trips_report.txt")


if __name__ == "__main__":
    main()
