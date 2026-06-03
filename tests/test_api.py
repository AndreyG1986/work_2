# tests/test_api.py
import unittest
from unittest.mock import patch, Mock
from src.api.aeroplanes_api import AeroplanesAPI


class TestAeroplanesAPI(unittest.TestCase):

    @patch('src.api.aeroplanes_api.get')
    def test_get_country_coordinates_success(self, mock_get):
        """Тест успешного получения координат страны"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'boundingbox': ['41.0', '83.0', '-141.0', '-52.0']}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates('Canada')

        self.assertIsNotNone(coords)
        self.assertEqual(coords[0], '41.0')

    @patch('src.api.aeroplanes_api.get')
    def test_get_country_coordinates_not_found(self, mock_get):
        """Тест: страна не найдена"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates('NonExistentCountry')

        self.assertIsNone(coords)


if __name__ == "__main__":
    unittest.main()