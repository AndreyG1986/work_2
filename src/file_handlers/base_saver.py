from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для работы с хранилищем данных"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавление информации о самолете в файл"""
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """Получение данных из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаление информации о самолете"""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Удаление всей информации"""
        pass