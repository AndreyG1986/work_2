# main.py
from src.api.aeroplanes_api import AeroplanesAPI
from src.models.aeroplane import Aeroplane
from src.file_handlers.json_saver import JSONSaver
from src.utils.filters import (
    filter_by_country,
    filter_by_altitude_range,
    get_top_aeroplanes,
    print_aeroplanes
)
from tqdm import tqdm


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("\n" + "=" * 60)
    print("     СБОР ДАННЫХ О САМОЛЕТАХ В ВОЗДУШНОМ ПРОСТРАНСТВЕ")
    print("=" * 60)

    # Создание экземпляра класса для работы с API
    api = AeroplanesAPI(timeout=90)  # Увеличиваем таймаут до 90 секунд для России

    # Ввод названия страны
    country = input("\nВведите название страны (например, Canada, Russia, Germany): ").strip()

    if not country:
        print("Название страны не может быть пустым")
        return

    print(f"\n🚀 Запрос данных о самолетах в {country}...")
    print("⏳ Это может занять 30-60 секунд для больших стран...")

    # Получение информации о самолетах
    aeroplanes_data = api.get_aeroplanes(country)

    if not aeroplanes_data or 'states' not in aeroplanes_data:
        print("❌ Не удалось получить данные о самолетах. Проверьте подключение или название страны.")
        return

    print("\n🔄 Преобразование данных в объекты...")
    # Преобразование набора данных в список объектов
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

    if not aeroplanes:
        print(f"❌ В воздушном пространстве {country} не найдено самолетов")
        return

    print(f"✅ Найдено самолетов: {len(aeroplanes)}")

    # Сохранение информации в файл
    print("\n💾 Сохранение данных в файл...")
    json_saver = JSONSaver()

    # Используем пакетное сохранение (быстрее)
    json_saver.add_aeroplanes_batch(aeroplanes)
    print(f"✅ Данные сохранены в файл {json_saver.filepath}")

    # Запрашиваем параметры фильтрации
    print("\n" + "=" * 60)
    print("📊 НАСТРОЙКА ФИЛЬТРАЦИИ")
    print("=" * 60)

    # Топ N самолетов по высоте
    top_n_input = input(f"\nВведите количество самолетов для вывода в топ N (1-{len(aeroplanes)}, по умолчанию 10): ")
    try:
        top_n = int(top_n_input) if top_n_input else 10
        top_n = min(max(1, top_n), len(aeroplanes))
    except ValueError:
        top_n = 10

    # Фильтрация по стране регистрации
    filter_input = input("Введите названия стран для фильтрации через пробел (или Enter для пропуска): ")
    filter_words = [w.strip() for w in filter_input.split()] if filter_input else []

    # Фильтрация по диапазону высот
    altitude_range = input("Введите диапазон высот (м), например '10000-20000' (или Enter для пропуска): ").strip()

    print("\n🔄 Применение фильтров...")

    # Применяем фильтры
    filtered_aeroplanes = filter_by_country(aeroplanes, filter_words)

    if altitude_range:
        ranged_aeroplanes = filter_by_altitude_range(filtered_aeroplanes, altitude_range)
    else:
        ranged_aeroplanes = filtered_aeroplanes

    # Получаем топ
    top_aeroplanes = get_top_aeroplanes(ranged_aeroplanes, top_n)

    # Выводим результат
    print("\n" + "=" * 60)
    print("📈 РЕЗУЛЬТАТЫ")
    print("=" * 60)
    print(f"Страна запроса: {country}")
    print(f"Фильтр по странам: {filter_words if filter_words else 'Нет'}")
    print(f"Фильтр по высоте: {altitude_range if altitude_range else 'Нет'}")
    print(f"Топ N: {top_n}")

    # Показываем топ самолетов
    print_aeroplanes(top_aeroplanes, max_display=top_n)

    # Дополнительная статистика
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)

    # Статистика по странам
    countries_stats = {}
    for plane in aeroplanes:
        country_name = plane.origin_country
        countries_stats[country_name] = countries_stats.get(country_name, 0) + 1

    top_countries = sorted(countries_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nТоп 5 стран по количеству самолетов:")
    for i, (country_name, count) in enumerate(top_countries, 1):
        print(f"  {i}. {country_name}: {count} самолетов")

    # Статистика по высоте
    if aeroplanes:
        max_alt = max(aeroplanes, key=lambda x: x.altitude)
        min_alt = min(aeroplanes, key=lambda x: x.altitude)
        avg_alt = sum(p.altitude for p in aeroplanes) / len(aeroplanes)

        print(f"\nСтатистика по высоте полета:")
        print(f"  📈 Максимальная: {max_alt.altitude:.0f} м ({max_alt.callsign})")
        print(f"  📉 Минимальная: {min_alt.altitude:.0f} м ({min_alt.callsign})")
        print(f"  📊 Средняя: {avg_alt:.0f} м")


def main():
    """Главная функция"""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
