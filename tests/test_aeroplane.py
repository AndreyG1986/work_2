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
        """Тест создания с некорректным позывным"""
        with self.assertRaises(ValueError):
            Aeroplane("", "United States", 268.79, 10203.18)

    def test_create_aeroplane_invalid_velocity(self):
        """Тест создания с отрицательной скоростью"""
        with self.assertRaises(ValueError):
            Aeroplane("UAL1621", "United States", -100, 10203.18)

    def test_comparison_by_altitude(self):
        """Тест сравнения самолетов по высоте"""
        plane1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        plane2 = Aeroplane("DLH431", "Germany", 250.00, 11000.00)

        self.assertTrue(plane2 > plane1)
        self.assertTrue(plane1 < plane2)

    def test_cast_from_api_state(self):
        """Тест преобразования из данных API"""
        api_state = [
            "abc123", "UAL1621", "United States", 1234567890,
            1234567890, -122.5, 37.5, 10203.18,
            False, 268.79, 270.0, 0.0,
            [], None, "1234", False, 0
        ]

        plane = Aeroplane.from_api_state(api_state)

        self.assertIsNotNone(plane)
        if plane:
            self.assertEqual(plane.callsign, "UAL1621")
            self.assertEqual(plane.origin_country, "United States")
            self.assertEqual(plane.velocity, 268.79)
            self.assertEqual(plane.altitude, 10203.18)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        plane_dict = plane.to_dict()

        self.assertEqual(plane_dict['callsign'], "UAL1621")
        self.assertEqual(plane_dict['origin_country'], "United States")
        self.assertEqual(plane_dict['velocity'], 268.79)
        self.assertEqual(plane_dict['altitude'], 10203.18)


if __name__ == "__main__":
    unittest.main()