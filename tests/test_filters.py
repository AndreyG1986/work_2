# tests/test_filters.py
import unittest
from src.models.aeroplane import Aeroplane
from src.utils.filters import (
    filter_by_country,
    filter_by_altitude_range,
    sort_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes
)


class TestFilters(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.planes = [
            Aeroplane("UAL1621", "United States", 268.79, 10203.18),
            Aeroplane("DLH431", "Germany", 250.00, 11000.00),
            Aeroplane("AFR123", "France", 245.50, 9500.00),
            Aeroplane("BAW456", "United Kingdom", 260.00, 10500.00),
            Aeroplane("AFL789", "Russia", 240.00, 8000.00),
            Aeroplane("SAS789", "Sweden", 230.00, 7000.00),
            Aeroplane("N/A", "Unknown", 0, 1000.00),
        ]

    def test_filter_by_country_single(self):
        """Тест фильтрации по одной стране"""
        result = filter_by_country(self.planes, ["Germany"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "DLH431")
        self.assertEqual(result[0].origin_country, "Germany")

    def test_filter_by_country_multiple(self):
        """Тест фильтрации по нескольким странам"""
        result = filter_by_country(self.planes, ["United States", "Germany"])
        self.assertEqual(len(result), 2)
        countries = {p.origin_country for p in result}
        self.assertEqual(countries, {"United States", "Germany"})

    def test_filter_by_country_case_insensitive(self):
        """Тест фильтрации без учета регистра"""
        result = filter_by_country(self.planes, ["united states"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].origin_country, "United States")

    def test_filter_by_country_empty_list(self):
        """Тест фильтрации с пустым списком стран"""
        result = filter_by_country(self.planes, [])
        self.assertEqual(len(result), len(self.planes))

    def test_filter_by_country_no_matches(self):
        """Тест фильтрации без совпадений"""
        result = filter_by_country(self.planes, ["NonExistentCountry"])
        self.assertEqual(len(result), 0)

    def test_filter_by_altitude_range_valid(self):
        """Тест фильтрации по диапазону высот (валидный)"""
        result = filter_by_altitude_range(self.planes, "9000-11000")
        # Ожидаем самолеты с высотой от 9000 до 11000
        # UAL1621 (10203.18), DLH431 (11000), BAW456 (10500), AFR123 (9500)
        self.assertEqual(len(result), 4)
        altitudes = [p.altitude for p in result]
        self.assertTrue(all(9000 <= alt <= 11000 for alt in altitudes))

    def test_filter_by_altitude_range_with_spaces(self):
        """Тест фильтрации с пробелами в диапазоне"""
        result = filter_by_altitude_range(self.planes, "9000 - 11000")
        self.assertEqual(len(result), 4)  # Все 4 самолета в диапазоне

    def test_filter_by_altitude_range_single_value(self):
        """Тест фильтрации с одним значением (точное совпадение)"""
        result = filter_by_altitude_range(self.planes, "8000")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "AFL789")

    def test_filter_by_altitude_range_lower_bound_only(self):
        """Тест фильтрации только с нижней границей (10000 и выше)"""
        result = filter_by_altitude_range(self.planes, "10000-")
        # Ожидаем самолеты с высотой >= 10000
        # UAL1621 (10203.18), DLH431 (11000), BAW456 (10500)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(p.altitude >= 10000 for p in result))

    def test_filter_by_altitude_range_upper_bound_only(self):
        """Тест фильтрации только с верхней границей (8000 и ниже)"""
        result = filter_by_altitude_range(self.planes, "-8000")
        # Ожидаем самолеты с высотой <= 8000
        # AFL789 (8000), SAS789 (7000), N/A (1000)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(p.altitude <= 8000 for p in result))

    def test_filter_by_altitude_range_empty(self):
        """Тест фильтрации с пустым диапазоном"""
        result = filter_by_altitude_range(self.planes, "")
        self.assertEqual(len(result), len(self.planes))

    def test_filter_by_altitude_range_invalid(self):
        """Тест фильтрации с неверным форматом"""
        result = filter_by_altitude_range(self.planes, "invalid")
        self.assertEqual(len(result), len(self.planes))  # Возвращает все самолеты

    def test_sort_by_altitude_descending(self):
        """Тест сортировки по убыванию высоты"""
        sorted_planes = sort_by_altitude(self.planes, reverse=True)
        altitudes = [p.altitude for p in sorted_planes]
        self.assertEqual(altitudes, [11000, 10500, 10203.18, 9500, 8000, 7000, 1000])

    def test_sort_by_altitude_ascending(self):
        """Тест сортировки по возрастанию высоты"""
        sorted_planes = sort_by_altitude(self.planes, reverse=False)
        altitudes = [p.altitude for p in sorted_planes]
        self.assertEqual(altitudes, [1000, 7000, 8000, 9500, 10203.18, 10500, 11000])

    def test_get_top_aeroplanes(self):
        """Тест получения топ N самолетов"""
        top_3 = get_top_aeroplanes(self.planes, 3)
        self.assertEqual(len(top_3), 3)
        self.assertEqual(top_3[0].callsign, "DLH431")  # Самый высокий
        self.assertEqual(top_3[1].callsign, "BAW456")
        self.assertEqual(top_3[2].callsign, "UAL1621")

    def test_get_top_aeroplanes_more_than_available(self):
        """Тест запроса большего количества, чем есть"""
        top_10 = get_top_aeroplanes(self.planes, 10)
        self.assertEqual(len(top_10), len(self.planes))

    def test_get_top_aeroplanes_zero(self):
        """Тест запроса 0 самолетов"""
        top_0 = get_top_aeroplanes(self.planes, 0)
        self.assertEqual(len(top_0), 0)

    def test_print_aeroplanes_empty_list(self):
        """Тест вывода пустого списка"""
        # Должно отработать без ошибок
        print_aeroplanes([])

    def test_print_aeroplanes_with_data(self):
        """Тест вывода списка самолетов"""
        # Должно отработать без ошибок
        print_aeroplanes(self.planes[:3])

    def test_print_aeroplanes_with_many(self):
        """Тест вывода большого списка (должен ограничиться 20)"""
        many_planes = self.planes * 10  # 70 самолетов
        print_aeroplanes(many_planes)  # Должно вывести только 20


if __name__ == "__main__":
    unittest.main()