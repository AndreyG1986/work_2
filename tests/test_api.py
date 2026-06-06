# tests/test_api.py
import unittest
from unittest.mock import patch, Mock
from src.api.aeroplanes_api import AeroplanesAPI


class TestAeroplanesAPI(unittest.TestCase):

    def setUp(self):
        self.api = AeroplanesAPI(timeout=30)

    @patch("src.api.aeroplanes_api.get")
    def test_get_country_coordinates_success(self, mock_get):
        """Тест успешного получения координат страны"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"boundingbox": ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"]}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        coords = self.api.get_country_coordinates("Canada")

        self.assertIsNotNone(coords)
        self.assertEqual(coords[0], "41.6765597")
        self.assertEqual(coords[1], "83.3362128")
        self.assertEqual(coords[2], "-141.0027500")
        self.assertEqual(coords[3], "-52.3237664")

    @patch("src.api.aeroplanes_api.get")
    def test_get_country_coordinates_not_found(self, mock_get):
        """Тест: страна не найдена"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        coords = self.api.get_country_coordinates("NonExistentCountry")

        self.assertIsNone(coords)

    @patch("src.api.aeroplanes_api.get")
    def test_get_country_coordinates_request_exception(self, mock_get):
        """Тест ошибки при запросе координат"""
        mock_get.side_effect = Exception("Network error")

        coords = self.api.get_country_coordinates("Canada")

        self.assertIsNone(coords)

    @patch("src.api.aeroplanes_api.get")
    def test_get_country_coordinates_timeout(self, mock_get):
        """Тест таймаута при запросе координат"""
        from requests import Timeout

        mock_get.side_effect = Timeout("Timeout")

        coords = self.api.get_country_coordinates("Canada")

        self.assertIsNone(coords)

    @patch("src.api.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    @patch("src.api.aeroplanes_api.get")
    def test_get_aeroplanes_success(self, mock_get, mock_get_coords):
        """Тест успешного получения самолетов"""
        # Мокаем координаты
        mock_get_coords.return_value = ["41.0", "83.0", "-141.0", "-52.0"]

        # Мокаем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            "time": 1234567890,
            "states": [
                ["abc123", "UAL1621", "United States", 1234567890, 1234567890, -122.5, 37.5, 10203.18, False, 268.79]
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api.get_aeroplanes("Canada")

        self.assertIsNotNone(result)
        self.assertIn("states", result)
        self.assertEqual(len(result["states"]), 1)

    @patch("src.api.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    def test_get_aeroplanes_no_coordinates(self, mock_get_coords):
        """Тест: координаты не найдены"""
        mock_get_coords.return_value = None

        result = self.api.get_aeroplanes("NonExistentCountry")

        self.assertIsNone(result)

    @patch("src.api.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    @patch("src.api.aeroplanes_api.get")
    def test_get_aeroplanes_request_exception(self, mock_get, mock_get_coords):
        """Тест ошибки при запросе самолетов"""
        mock_get_coords.return_value = ["41.0", "83.0", "-141.0", "-52.0"]
        mock_get.side_effect = Exception("Network error")

        result = self.api.get_aeroplanes("Canada")

        self.assertIsNone(result)

    @patch("src.api.aeroplanes_api.AeroplanesAPI.get_country_coordinates")
    @patch("src.api.aeroplanes_api.get")
    def test_get_aeroplanes_timeout(self, mock_get, mock_get_coords):
        """Тест таймаута при запросе самолетов"""
        from requests import Timeout

        mock_get_coords.return_value = ["41.0", "83.0", "-141.0", "-52.0"]
        mock_get.side_effect = Timeout("Timeout")

        result = self.api.get_aeroplanes("Canada")

        self.assertIsNone(result)

    @patch("src.api.aeroplanes_api.get")
    def test_get_aeroplanes_invalid_json_response(self, mock_get):
        """Тест невалидного JSON ответа"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api.get_aeroplanes("Canada")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
