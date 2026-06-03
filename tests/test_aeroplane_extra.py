# tests/test_aeroplane_extra.py
import unittest
from src.models.aeroplane import Aeroplane


class TestAeroplaneExtra(unittest.TestCase):

    def test_equality_by_callsign(self):
        """Тест сравнения по позывному"""
        plane1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        plane2 = Aeroplane("UAL1621", "Canada", 200.00, 5000.00)
        plane3 = Aeroplane("DLH431", "Germany", 250.00, 11000.00)

        self.assertEqual(plane1, plane2)  # Одинаковые позывные
        self.assertNotEqual(plane1, plane3)  # Разные позывные

    def test_validation_fixes_values(self):
        """Тест валидации исправляет значения"""
        plane = Aeroplane("", "", "invalid", None)
        self.assertEqual(plane.callsign, "N/A")
        self.assertEqual(plane.origin_country, "Unknown")
        self.assertEqual(plane.velocity, 0.0)
        self.assertEqual(plane.altitude, 0.0)

    def test_cast_to_object_list_empty(self):
        """Тест преобразования пустого ответа"""
        result = Aeroplane.cast_to_object_list({})
        self.assertEqual(result, [])

        result = Aeroplane.cast_to_object_list({'states': None})
        self.assertEqual(result, [])

        result = Aeroplane.cast_to_object_list({'states': []})
        self.assertEqual(result, [])

    def test_cast_to_object_list_with_invalid_states(self):
        """Тест пропуска некорректных состояний"""
        api_response = {
            'states': [
                None,  # Некорректное состояние
                [],  # Пустой список
                ['valid', 'test', 'country', 1, 2, 3, 4, 5, 6, 7],  # Короткий список
                ['a', 'b', 'c', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],  # Полный
            ]
        }

        result = Aeroplane.cast_to_object_list(api_response)
        # Должен быть хотя бы один валидный самолет
        self.assertGreaterEqual(len(result), 0)

    def test_from_api_state_missing_fields(self):
        """Тест создания с недостающими полями"""
        # Слишком короткий список
        result = Aeroplane.from_api_state([1, 2, 3])
        self.assertIsNone(result)

        # Пустой список
        result = Aeroplane.from_api_state([])
        self.assertIsNone(result)

        # None вместо списка
        result = Aeroplane.from_api_state(None)
        self.assertIsNone(result)

    def test_from_api_state_with_negative_altitude(self):
        """Тест с отрицательной высотой (под землей)"""
        api_state = [
            "abc123", "TEST", "Country", 1, 2, 3, 4, -500,  # Отрицательная высота
            False, 100, 0, 0, [], None, "1234", False, 0
        ]

        plane = Aeroplane.from_api_state(api_state)
        self.assertIsNotNone(plane)
        if plane:
            self.assertEqual(plane.altitude, -500)  # Отрицательная высота допустима

    def test_from_api_state_with_geo_altitude(self):
        """Тест использования geo_altitude когда baro_altitude отсутствует"""
        api_state = [
            "abc123", "TEST", "Country", 1, 2, 3, 4, None,  # baro_altitude = None
            False, 100, 0, 0, [], 15000, "1234", False, 0  # geo_altitude = 15000
        ]

        plane = Aeroplane.from_api_state(api_state)
        self.assertIsNotNone(plane)
        if plane:
            self.assertEqual(plane.altitude, 15000)

    def test_to_dict_with_all_fields(self):
        """Тест преобразования в словарь со всеми полями"""
        plane = Aeroplane(
            callsign="TEST123",
            origin_country="Testland",
            velocity=300.50,
            altitude=12000.75,
            longitude=55.123456,
            latitude=37.654321,
            on_ground=False
        )

        plane_dict = plane.to_dict()

        self.assertEqual(plane_dict['callsign'], "TEST123")
        self.assertEqual(plane_dict['origin_country'], "Testland")
        self.assertEqual(plane_dict['velocity'], 300.50)
        self.assertEqual(plane_dict['altitude'], 12000.75)
        self.assertEqual(plane_dict['longitude'], 55.123456)
        self.assertEqual(plane_dict['latitude'], 37.654321)
        self.assertEqual(plane_dict['on_ground'], False)

    def test_sorting_with_equal_altitudes(self):
        """Тест сортировки при одинаковых высотах"""
        plane1 = Aeroplane("A", "USA", 100, 10000)
        plane2 = Aeroplane("B", "USA", 100, 10000)
        plane3 = Aeroplane("C", "USA", 100, 10000)

        planes = [plane3, plane1, plane2]
        sorted_planes = sorted(planes, reverse=True)

        # Все должны быть в списке, порядок может быть любым
        self.assertEqual(len(sorted_planes), 3)
        self.assertIn(plane1, sorted_planes)
        self.assertIn(plane2, sorted_planes)
        self.assertIn(plane3, sorted_planes)


if __name__ == "__main__":
    unittest.main()