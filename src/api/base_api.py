from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервисов"""

    @abstractmethod
    def get_country_coordinates(self, country: str) -> Optional[List[str]]:
        """
        Получение географических координат страны

        Args:
            country: Название страны

        Returns:
            Список [юг, север, запад, восток] или None
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Получение информации о самолетах в воздушном пространстве страны

        Args:
            country: Название страны

        Returns:
            Словарь с данными о самолетах
        """
        pass