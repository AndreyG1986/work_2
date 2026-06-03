# tests/test_main.py
import unittest
from unittest.mock import patch, Mock
from src.main import user_interaction


class TestMain(unittest.TestCase):

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_success(self, mock_print, mock_input, mock_api_class):
        """Тест успешного выполнения user_interaction"""
        # Настройка моков для input
        mock_input.side_effect = ['Russia', '5', '', '']

        # Настройка мока API
        mock_api = Mock()
        mock_api_class.return_value = mock_api

        # Мокаем ответ API
        mock_api.get_aeroplanes.return_value = {
            'states': [
                ['abc123', 'UAL1621', 'United States', 1, 2, 3, 4, 10000, False, 250, 0],
                ['def456', 'DLH431', 'Germany', 1, 2, 3, 4, 11000, False, 260, 0],
            ]
        }

        # Запускаем функцию
        user_interaction()

        # Проверяем, что API был вызван
        mock_api.get_aeroplanes.assert_called_once_with('Russia')

        # Проверяем, что print вызывался (хотя бы один раз)
        mock_print.assert_called()

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_country_not_found(self, mock_print, mock_input, mock_api_class):
        """Тест: страна не найдена"""
        mock_input.side_effect = ['NonExistentCountry', '', '', '']

        mock_api = Mock()
        mock_api_class.return_value = mock_api
        mock_api.get_aeroplanes.return_value = None

        user_interaction()

        # Проверяем, что было выведено сообщение об ошибке
        mock_print.assert_any_call(
            '❌ Не удалось получить данные о самолетах. Проверьте подключение или название страны.')

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_empty_country(self, mock_print, mock_input, mock_api_class):
        """Тест: пустое название страны"""
        mock_input.side_effect = ['', '', '', '']

        user_interaction()

        mock_print.assert_any_call('Название страны не может быть пустым')
        mock_api_class.assert_not_called()  # API не должен вызываться

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_no_aircraft(self, mock_print, mock_input, mock_api_class):
        """Тест: нет самолетов в воздушном пространстве"""
        mock_input.side_effect = ['Russia', '5', '', '']

        mock_api = Mock()
        mock_api_class.return_value = mock_api
        mock_api.get_aeroplanes.return_value = {'states': []}

        user_interaction()

        mock_print.assert_any_call('❌ В воздушном пространстве Russia не найдено самолетов')

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_with_filters(self, mock_print, mock_input, mock_api_class):
        """Тест с фильтрацией по странам и высоте"""
        mock_input.side_effect = [
            'Russia',  # страна
            '5',  # топ N
            'United States Germany',  # фильтр по странам
            '10000-20000'  # фильтр по высоте
        ]

        mock_api = Mock()
        mock_api_class.return_value = mock_api
        mock_api.get_aeroplanes.return_value = {
            'states': [
                ['abc123', 'UAL1621', 'United States', 1, 2, 3, 4, 15000, False, 250, 0],
                ['def456', 'DLH431', 'Germany', 1, 2, 3, 4, 12000, False, 260, 0],
                ['ghi789', 'AFR123', 'France', 1, 2, 3, 4, 8000, False, 240, 0],
            ]
        }

        user_interaction()

        # Проверяем, что API был вызван
        mock_api.get_aeroplanes.assert_called_once_with('Russia')
        mock_print.assert_called()

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_invalid_top_n(self, mock_print, mock_input, mock_api_class):
        """Тест: неверное значение топ N"""
        mock_input.side_effect = [
            'Russia',  # страна
            'invalid',  # неверное значение топ N
            '',  # фильтр по странам (пусто)
            ''  # фильтр по высоте (пусто)
        ]

        mock_api = Mock()
        mock_api_class.return_value = mock_api
        mock_api.get_aeroplanes.return_value = {
            'states': [
                ['abc123', 'UAL1621', 'United States', 1, 2, 3, 4, 10000, False, 250, 0],
            ]
        }

        user_interaction()

        # Должно выполниться без ошибок (используется значение по умолчанию 10)
        mock_api.get_aeroplanes.assert_called_once()

    @patch('src.main.AeroplanesAPI')
    @patch('src.main.input')
    @patch('src.main.print')
    def test_user_interaction_keyboard_interrupt(self, mock_print, mock_input, mock_api_class):
        """Тест прерывания клавиатурой"""
        mock_input.side_effect = KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            user_interaction()


if __name__ == "__main__":
    unittest.main()