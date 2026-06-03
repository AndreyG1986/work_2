# src/api/base_api.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import requests


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с внешними API"""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Инициализация базового API клиента

        Args:
            base_url: Базовый URL API сервиса
            timeout: Таймаут запросов в секундах
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CourseWork/1.0 (Student Project)"})

    @abstractmethod
    def get_country_coordinates(self, country: str) -> Optional[List[str]]:
        """Получение географических координат страны"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> Optional[Dict[str, Any]]:
        """Получение информации о самолетах в воздушном пространстве страны"""
        pass

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Выполнение HTTP запроса к API

        Args:
            endpoint: Конечная точка API
            params: Параметры запроса

        Returns:
            JSON ответа или None при ошибке
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к {url}: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return None

    def close(self):
        """Закрытие сессии"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
