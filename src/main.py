from src.api.aeroplanes_api import AeroplanesAPI
from src.models.aeroplane import Aeroplane
from src.file_handlers.json_saver import JSONSaver
from src.utils.filters import (
    filter_by_country,
    filter_by_altitude_range,
    sort_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes
)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("\n" + "=" * 60)
    print("     СБОР ДАННЫХ О САМОЛЕТАХ В ВОЗДУШНОМ ПРОСТРАНСТВЕ")
    print("=" * 60)

    # Создание экземпляра класса для работы с API
    api = AeroplanesAPI()

    # Ввод названия страны
    country = input("\nВведите название страны (например, Canada, Russia, Germany): ").strip()

    if not country:
        print("Название страны не может быть пустым")
        return

    print(f"\nЗапрос данных о самолетах в {country}...")

    # Получение информации о самолетах
    aeroplanes_data = api.get_aeroplanes(country)

    if not aeroplanes_data or 'states' not in aeroplanes_data:
        print("Не удалось получить данные о самолетах. Проверьте подключение или название страны.")
        return

    # Преобразование набора данных в список объектов
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

    if not aeroplanes:
        print(f"В воздушном пространстве {country} не найдено самолетов")
        return

    print(f"Найдено самолетов: {len(aeroplanes)}")

    # Сохранение информации в файл
    json_saver = JSONSaver()
    for aeroplane in aeroplanes:
        json_saver.add_aeroplane(aeroplane)
    print(f"Данные сохранены в файл {json_saver.filepath}")

    # Топ N самолетов по высоте
    top_n_input = input(f"\nВведите количество самолетов для вывода в топ N (макс {len(aeroplanes)}): ")
    try:
        top_n = int(top_n_input) if top_n_input else 10
        top_n = min(top_n, len(aeroplanes))
    except ValueError:
        top_n = 10

    # Фильтрация по стране регистрации
    filter_input = input("Введите названия стран для фильтрации через пробел (или оставьте пустым): ")
    filter_words = [w.strip() for w in filter_input.split()] if filter_input else []

    # Фильтрация по диапазону высот
    altitude_range = input("Введите диапазон высот (м), например '10000-20000' (или оставьте пустым): ").strip()

    # Применяем фильтры
    filtered_aeroplanes = filter_by_country(aeroplanes, filter_words)

    if altitude_range:
        ranged_aeroplanes = filter_by_altitude_range(filtered_aeroplanes, altitude_range)
    else:
        ranged_aeroplanes = filtered_aeroplanes

    # Сортируем и получаем топ
    top_aeroplanes = get_top_aeroplanes(ranged_aeroplanes, top_n)

    # Выводим результат
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ")
    print(f"Страна запроса: {country}")
    print(f"Фильтр по странам: {filter_words if filter_words else 'Нет'}")
    print(f"Фильтр по высоте: {altitude_range if altitude_range else 'Нет'}")
    print(f"Топ N: {top_n}")
    print_aeroplanes(top_aeroplanes)

    # Демонстрация работы с удалением (опционально)
    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ")
    print("=" * 60)

    # Получаем самолеты из файла по фильтру
    saved_by_country = json_saver.get_aeroplanes(origin_country="United States")
    print(f"\nСамолеты из файла с регистрацией в США: {len(saved_by_country)}")

    # Пример работы конструктора класса с одним самолетом
    example_aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    print(f"\nПример создания самолета вручную: {example_aeroplane.callsign}")
    print(f"  Скорость: {example_aeroplane.velocity} м/с")
    print(f"  Высота: {example_aeroplane.altitude} м")


def main():
    """Главная функция"""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")


if __name__ == "__main__":
    main()