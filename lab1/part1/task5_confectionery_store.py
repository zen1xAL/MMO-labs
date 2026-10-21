"""
Лабораторная работа №1. Часть 1.
Вариант 7. Задание 5.

Условие:
Реализуйте программу «Кондитерская» (6 пунктов меню).
Словарь: [состав, цена/100г, вес_г].
1. Просмотр описания: название – описание
2. Просмотр цены: название – цена
3. Просмотр количества: название – количество
4. Всю информацию
5. Покупка (название, вес, 'n' для выхода, расчёт чека и остатков)
6. До свидания
"""

import sys
from typing import Dict, List, Tuple


def get_initial_catalog() -> Dict[str, List]:
    return {
        "Торт 'Наполеон'": [
            "Слоеные коржи, заварной крем",
            4.50,
            2000,
        ],
        "Пирожное 'Эклер'": [
            "Заварное тесто, крем, шоколад",
            3.20,
            1200,
        ],
        "Маффин шоколадный": [
            "Шоколадный бисквит, кусочки шоколада",
            2.80,
            1500,
        ],
        "Чизкейк 'Нью-Йорк'": [
            "Песочная основа, крем-чиз",
            5.00,
            1800,
        ],
        "Круассан классич.": [
            "Французское слоеное тесто",
            2.20,
            900,
        ],
    }


def show_descriptions(catalog: Dict[str, List]) -> None:
    print("\n--- 1. Описание продукции ---")
    for name, data in catalog.items():
        print(f"• {name}: {data[0]}")


def show_prices(catalog: Dict[str, List]) -> None:
    print("\n--- 2. Цены на продукцию (за 100 грамм) ---")
    for name, data in catalog.items():
        print(f"• {name}: {data[1]:.2f} руб./100г")


def show_quantities(catalog: Dict[str, List]) -> None:
    print("\n--- 3. Количество продукции в наличии (в граммах) ---")
    for name, data in catalog.items():
        print(f"• {name}: {data[2]} г")


def show_all_info(catalog: Dict[str, List]) -> None:
    print("\n--- 4. Полный ассортимент кондитерской ---")
    print(f"{'Товар':<15} | {'Цена/100г':<10} | {'Остаток':<7} | {'Состав'}")
    print("-" * 72)
    for name, data in catalog.items():
        print(f"{name:<15} | {data[1]:>6.2f} руб | {data[2]:>5} г | {data[0]}")


def process_purchase(
    catalog: Dict[str, List], mock_inputs: List[str] = None
) -> None:
    print("\n--- 5. Покупка товаров ---")
    print("Вводите название товара и вес в граммах. 'n' - выход.")

    mock_idx = 0

    def custom_input(prompt: str) -> str:
        nonlocal mock_idx
        if mock_inputs is not None:
            if mock_idx < len(mock_inputs):
                val = mock_inputs[mock_idx]
                mock_idx += 1
                print(f"{prompt}{val}")
                return val
            return "n"
        return input(prompt)

    cart: List[Tuple[str, float, float]] = []
    total_cost = 0.0

    while True:
        prod = custom_input("\nТовар ('n' для завершения): ").strip()
        if prod.lower() == "n":
            break

        matched = None
        for key in catalog:
            if key.lower() == prod.lower():
                matched = key
                break

        if not matched:
            print(f"Товар '{prod}' не найден в ассортименте!")
            continue

        stock = catalog[matched][2]
        if stock <= 0:
            print(f"Товар '{matched}' закончился на складе.")
            continue

        qty_str = custom_input(
            f"Вес в граммах (доступно {stock} г): "
        ).strip()
        if qty_str.lower() == "n":
            break

        try:
            qty = float(qty_str)
            if qty <= 0 or qty > stock:
                print(f"Недопустимое количество! В наличии: {stock} г.")
                continue

            cost = (catalog[matched][1] / 100.0) * qty
            catalog[matched][2] -= qty
            total_cost += cost
            cart.append((matched, qty, cost))
            print(f"Добавлено: {matched} - {qty:.0f} г на {cost:.2f} руб.")

        except ValueError:
            print("Ошибка: введите число.")

    print("\n" + "=" * 45)
    print("ИТОГОВЫЙ ЧЕК:")
    print("=" * 45)
    for item, w, c in cart:
        print(f"• {item:<20}: {w:>5.0f} г  = {c:>6.2f} руб.")
    print("-" * 45)
    print(f"Итого к оплате: {total_cost:.2f} руб.")

    print("\nОстатки на складе после покупки:")
    for name, data in catalog.items():
        print(f"  {name:<20}: {data[2]} г")


def run_confectionery(mock_actions: List[str] = None) -> None:
    catalog = get_initial_catalog()
    act_idx = 0

    def get_action() -> str:
        nonlocal act_idx
        if mock_actions is not None:
            if act_idx < len(mock_actions):
                val = mock_actions[act_idx]
                act_idx += 1
                return val
            return "6"
        return input("\nВыберите пункт меню (1-6): ").strip()

    while True:
        print("\n" + "=" * 45)
        print("     КОНДИТЕРСКАЯ 'СЛАДКИЙ УГОЛОК'")
        print("=" * 45)
        print("1. Просмотр описания продукции")
        print("2. Просмотр цен")
        print("3. Просмотр количества")
        print("4. Просмотр всей информации")
        print("5. Покупка")
        print("6. До свидания")

        choice = get_action()
        print(f"Выбран пункт: {choice}")

        if choice == "1":
            show_descriptions(catalog)
        elif choice == "2":
            show_prices(catalog)
        elif choice == "3":
            show_quantities(catalog)
        elif choice == "4":
            show_all_info(catalog)
        elif choice == "5":
            if mock_actions is not None:
                test_cart = [
                    "Пирожное 'Эклер'", "400",
                    "Торт 'Наполеон'", "500",
                    "n"
                ]
                process_purchase(catalog, mock_inputs=test_cart)
            else:
                process_purchase(catalog)
        elif choice == "6":
            print("\nСпасибо за визит! До свидания!")
            break
        else:
            print("Введите цифру от 1 до 6.")


def main() -> None:
    if "--demo" in sys.argv or not sys.stdin.isatty():
        run_confectionery(mock_actions=["4", "5", "6"])
    else:
        run_confectionery()


if __name__ == "__main__":
    main()
