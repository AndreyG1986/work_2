# src/utils/filters.py
from typing import List, Tuple, Optional
from src.models.aeroplane import Aeroplane


def filter_by_country(aeroplanes: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """
    Фильтрация самолетов по стране регистрации

    Args:
        aeroplanes: Список самолетов
        countries: Список стран для фильтрации

    Returns:
        Отфильтрованный список
    """
    if not countries:
        return aeroplanes

    countries_lower = [c.lower().strip() for c in countries]

    return [
        a for a in aeroplanes
        if a.origin_country.lower() in countries_lower
    ]


def filter_by_altitude_range(aeroplanes: List[Aeroplane],
                             altitude_range: str) -> List[Aeroplane]:
    """
    Фильтрация самолетов по диапазону высот

    Args:
        aeroplanes: Список самолетов
        altitude_range: Строка вида "min - max" или "min-max"

    Returns:
        Отфильтрованный список
    """
    if not altitude_range:
        return aeroplanes

    try:
        # Парсим диапазон
        altitude_range = altitude_range.replace(' ', '')
        if '-' in altitude_range:
            parts = altitude_range.split('-')
            min_alt = float(parts[0]) if parts[0] else -float('inf')
            max_alt = float(parts[1]) if parts[1] else float('inf')
        else:
            # Если только одно число - ищем точное совпадение
            min_alt = max_alt = float(altitude_range)

        return [
            a for a in aeroplanes
            if min_alt <= a.altitude <= max_alt
        ]
    except (ValueError, TypeError):
        print("Неверный формат диапазона высот. Используйте формат: 10000-20000")
        return aeroplanes


def sort_by_altitude(aeroplanes: List[Aeroplane], reverse: bool = True) -> List[Aeroplane]:
    """
    Сортировка самолетов по высоте

    Args:
        aeroplanes: Список самолетов
        reverse: True - по убыванию, False - по возрастанию

    Returns:
        Отсортированный список
    """
    return sorted(aeroplanes, key=lambda x: x.altitude, reverse=reverse)


def get_top_aeroplanes(aeroplanes: List[Aeroplane], n: int) -> List[Aeroplane]:
    """Получение топ N самолетов по высоте"""
    sorted_aeroplanes = sort_by_altitude(aeroplanes, reverse=True)
    return sorted_aeroplanes[:n]


def print_aeroplanes(aeroplanes: List[Aeroplane], max_display: int = 20) -> None:
    """
    Вывод информации о самолетах в консоль

    Args:
        aeroplanes: Список самолетов
        max_display: Максимальное количество для отображения
    """
    if not aeroplanes:
        print("Самолеты не найдены")
        return

    print(f"\n{'=' * 80}")
    print(f"Найдено самолетов: {len(aeroplanes)}")
    print(f"{'=' * 80}")

    display_count = min(len(aeroplanes), max_display)
    for i, plane in enumerate(aeroplanes[:display_count], 1):
        print(f"\n{i}. {plane.callsign}")
        print(f"   Страна регистрации: {plane.origin_country}")
        print(f"   Скорость: {plane.velocity:.2f} м/с ({plane.velocity * 3.6:.2f} км/ч)")
        print(f"   Высота: {plane.altitude:.2f} м")
        if plane.longitude and plane.latitude:
            print(f"   Координаты: ({plane.latitude:.4f}, {plane.longitude:.4f})")
        print(f"   На земле: {'Да' if plane.on_ground else 'Нет'}")

    if len(aeroplanes) > max_display:
        print(f"\n... и еще {len(aeroplanes) - max_display} самолетов")
