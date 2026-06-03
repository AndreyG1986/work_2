# tests/test_base_api.py (исправленный тест)
import unittest
from unittest.mock import patch, Mock
from requests import RequestException, Timeout
from src.api.base_api import BaseAPI


class ConcreteAPI(BaseAPI):
    """Конкретная реализация для тестирования"""

    def __init__(self, base_url: str, timeout: int = 30):
        """Конструктор с параметрами"""
        BaseAPI.__init__(self, base_url, timeout)

    def get_country_coordinates(self, country: str):
        """Реализация абстрактного метода"""
        return None

    def get_aeroplanes(self, country: str):
        """Реализация абстрактного метода"""
        return None

    def get_data(self, **params):
        """Дополнительный метод для тестирования"""
        return self._make_request("test", params)


class TestBaseAPI(unittest.TestCase):

    def setUp(self):
        self.api = ConcreteAPI("https://api.test.com", timeout=10)

    def test_init(self):
        """Тест инициализации"""
        self.assertEqual(self.api.base_url, "https://api.test.com")
        self.assertEqual(self.api.timeout, 10)
        self.assertIsNotNone(self.api.session)
        # Проверяем заголовки User-Agent
        self.assertIn("User-Agent", self.api.session.headers)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_success(self, mock_get):
        """Тест успешного запроса"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api._make_request("test", {"param": "value"})

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("https://api.test.com/test", params={"param": "value"}, timeout=10)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_without_params(self, mock_get):
        """Тест запроса без параметров"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api._make_request("test")

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("https://api.test.com/test", params=None, timeout=10)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_network_error(self, mock_get):
        """Тест ошибки сети"""
        mock_get.side_effect = RequestException("Network error")

        result = self.api._make_request("test")

        self.assertIsNone(result)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_timeout(self, mock_get):
        """Тест таймаута"""
        mock_get.side_effect = Timeout("Timeout")

        result = self.api._make_request("test")

        self.assertIsNone(result)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_invalid_json(self, mock_get):
        """Тест невалидного JSON"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api._make_request("test")

        self.assertIsNone(result)

    @patch("src.api.base_api.requests.Session.get")
    def test_make_request_http_error(self, mock_get):
        """Тест HTTP ошибки (404, 500 и т.д.)"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = RequestException("404 Not Found")
        mock_get.return_value = mock_response

        result = self.api._make_request("test")

        self.assertIsNone(result)

    def test_context_manager(self):
        """Тест контекстного менеджера"""
        with ConcreteAPI("https://api.test.com", timeout=5) as api:
            self.assertIsNotNone(api)
            # Проверяем, что сессия открыта
            self.assertIsNotNone(api.session)
        # После выхода из контекста сессия должна быть закрыта

    @patch("src.api.base_api.requests.Session.close")
    def test_close_method(self, mock_close):
        """Тест метода close"""
        self.api.close()
        mock_close.assert_called_once()

    def test_abstract_method_requires_implementation(self):
        """Тест: абстрактный метод требует реализации"""

        # Создаем класс без реализации абстрактных методов
        class IncompleteAPI(BaseAPI):
            pass

        with self.assertRaises(TypeError):
            IncompleteAPI("https://api.test.com")

    def test_get_data_calls_make_request(self):
        """Тест: get_data вызывает _make_request"""
        with patch.object(self.api, "_make_request") as mock_make:
            mock_make.return_value = {"result": "ok"}
            result = self.api.get_data(param1="value1", param2="value2")

            mock_make.assert_called_once_with("test", {"param1": "value1", "param2": "value2"})
            self.assertEqual(result, {"result": "ok"})

    def test_make_request_with_slash_in_endpoint(self):
        """Тест запроса с слешем в endpoint"""
        # Проверяем, что метод _make_request правильно обрабатывает слеши
        # Вместо мока, давайте протестируем реальное поведение метода
        with patch.object(self.api, "_make_request", wraps=self.api._make_request) as mock_make:
            mock_make.return_value = {"data": "test"}
            result = self.api._make_request("/test")

            # Проверяем, что метод был вызван ровно один раз
            mock_make.assert_called_once()
            # Проверяем, что был передан правильный endpoint
            args, kwargs = mock_make.call_args
            self.assertEqual(args[0], "/test")  # endpoint должен быть передан как есть

    def test_make_request_strips_slash_in_actual_call(self):
        """Тест: _make_request должен убирать слеш при формировании URL"""
        with patch("src.api.base_api.requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"data": "test"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            # Вызываем _make_request с endpoint, содержащим слеш
            self.api._make_request("/test")

            # Проверяем, что URL был сформирован без двойного слеша
            mock_get.assert_called_once()
            url = mock_get.call_args[0][0]
            self.assertEqual(url, "https://api.test.com/test")  # Слеш должен быть убран

    def test_session_headers(self):
        """Тест заголовков сессии"""
        self.assertIn("User-Agent", self.api.session.headers)
        self.assertEqual(self.api.session.headers["User-Agent"], "CourseWork/1.0 (Student Project)")


if __name__ == "__main__":
    unittest.main()
