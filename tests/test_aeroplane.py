# tests/test_aeroplane.py
import unittest
from src.models.aeroplane import Aeroplane


class TestAeroplane(unittest.TestCase):

    def test_create_aeroplane_valid(self):
        """Тест создания корректного самолета"""
        plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        self.assertEqual(plane.callsign, "UAL1621")
        self.assertEqual(plane.origin_country, "United States")
        self.assertEqual(plane.velocity, 268.79)
        self.assertEqual(plane.altitude, 10203.18)

    def test_create_aeroplane_invalid_callsign(self):
        """Тест создания с некорректным позывным - должен заменяться на N/A"""
        # Пустой позывной - должен стать "N/A"
        plane = Aeroplane("", "United States", 268.79, 10203.18)
        self.assertEqual(plane.callsign, "N/A")
        self.assertEqual(plane.origin_country, "United States")

        # None вместо позывного
        plane2 = Aeroplane(None, "United States", 268.79, 10203.18)
        self.assertEqual(plane2.callsign, "N/A")

        # Пробелы вместо позывного
        plane3 = Aeroplane("   ", "United States", 268.79, 10203.18)
        self.assertEqual(plane3.callsign, "N/A")

    def test_create_aeroplane_invalid_velocity(self):
        """Тест создания с отрицательной скоростью - должна заменяться на 0"""
        # Отрицательная скорость - должна стать 0
        plane = Aeroplane("UAL1621", "United States", -100, 10203.18)
        self.assertEqual(plane.velocity, 0)

        # Нечисловое значение скорости
        plane2 = Aeroplane("UAL1621", "United States", None, 10203.18)
        self.assertEqual(plane2.velocity, 0)

        # Строка вместо числа
        plane3 = Aeroplane("UAL1621", "United States", "abc", 10203.18)
        self.assertEqual(plane3.velocity, 0)

    def test_create_aeroplane_invalid_country(self):
        """Тест создания с некорректной страной - должна заменяться на Unknown"""
        plane = Aeroplane("UAL1621", "", 268.79, 10203.18)
        self.assertEqual(plane.origin_country, "Unknown")

        plane2 = Aeroplane("UAL1621", None, 268.79, 10203.18)
        self.assertEqual(plane2.origin_country, "Unknown")

    def test_comparison_by_altitude(self):
        """Тест сравнения самолетов по высоте"""
        plane1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        plane2 = Aeroplane("DLH431", "Germany", 250.00, 11000.00)

        self.assertTrue(plane2 > plane1)
        self.assertTrue(plane1 < plane2)

        # Тест равенства по позывному
        plane3 = Aeroplane("UAL1621", "Canada", 300.00, 5000.00)
        self.assertEqual(plane1, plane3)  # Одинаковые позывные

    def test_cast_from_api_state(self):
        """Тест преобразования из данных API"""
        api_state = [
            "abc123",  # icao24
            "UAL1621",  # callsign
            "United States",  # origin_country
            1234567890,  # time_position
            1234567890,  # last_contact
            -122.5,  # longitude
            37.5,  # latitude
            10203.18,  # baro_altitude
            False,  # on_ground
            268.79,  # velocity (индекс 9)
            270.0,  # true_track
            0.0,  # vertical_rate
            [],  # sensors
            None,  # geo_altitude
            "1234",  # squawk
            False,  # spi
            0,  # position_source
        ]

        plane = Aeroplane.from_api_state(api_state)

        self.assertIsNotNone(plane)
        if plane:
            self.assertEqual(plane.callsign, "UAL1621")
            self.assertEqual(plane.origin_country, "United States")
            self.assertEqual(plane.velocity, 268.79)
            self.assertEqual(plane.altitude, 10203.18)
            self.assertEqual(plane.longitude, -122.5)
            self.assertEqual(plane.latitude, 37.5)
            self.assertFalse(plane.on_ground)

    def test_cast_from_api_state_with_none_values(self):
        """Тест преобразования из данных API с None значениями"""
        api_state = [
            "abc123",
            None,  # callsign = None
            "Unknown",
            None,
            None,
            None,
            None,
            None,
            None,
            None,  # velocity = None
            None,
            None,
            [],
            None,
            None,
            False,
            0,
        ]

        plane = Aeroplane.from_api_state(api_state)

        self.assertIsNotNone(plane)
        if plane:
            # Проверяем значения по умолчанию
            self.assertEqual(plane.callsign, "N/A")
            self.assertEqual(plane.velocity, 0)
            self.assertEqual(plane.altitude, 0)

    def test_cast_from_api_state_with_empty_callsign(self):
        """Тест преобразования с пустым позывным"""
        api_state = [
            "abc123",
            "",  # пустой callsign
            "United States",
            1234567890,
            1234567890,
            -122.5,
            37.5,
            10203.18,
            False,
            268.79,
            270.0,
            0.0,
            [],
            None,
            "1234",
            False,
            0,
        ]

        plane = Aeroplane.from_api_state(api_state)

        self.assertIsNotNone(plane)
        if plane:
            self.assertEqual(plane.callsign, "N/A")
            self.assertEqual(plane.velocity, 268.79)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        plane_dict = plane.to_dict()

        self.assertEqual(plane_dict["callsign"], "UAL1621")
        self.assertEqual(plane_dict["origin_country"], "United States")
        self.assertEqual(plane_dict["velocity"], 268.79)
        self.assertEqual(plane_dict["altitude"], 10203.18)

        # Проверяем опциональные поля
        self.assertIsNone(plane_dict.get("longitude"))
        self.assertIsNone(plane_dict.get("latitude"))
        self.assertIsNone(plane_dict.get("on_ground"))

    def test_sorting(self):
        """Тест сортировки списка самолетов"""
        planes = [
            Aeroplane("A", "USA", 100, 5000),
            Aeroplane("B", "USA", 100, 10000),
            Aeroplane("C", "USA", 100, 3000),
            Aeroplane("D", "USA", 100, 8000),
        ]

        sorted_planes = sorted(planes, reverse=True)

        self.assertEqual(sorted_planes[0].altitude, 10000)
        self.assertEqual(sorted_planes[1].altitude, 8000)
        self.assertEqual(sorted_planes[2].altitude, 5000)
        self.assertEqual(sorted_planes[3].altitude, 3000)


if __name__ == "__main__":
    unittest.main()