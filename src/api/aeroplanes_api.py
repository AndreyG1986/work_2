from typing import Dict, Any, Optional, List
from requests import get
from src.api.base_api import BaseAPI


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API сервисов Nominatim и OpenSky"""

    def __init__(self):
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api/states/all'
        self.last_response = None

    def get_country_coordinates(self, country: str) -> Optional[List[str]]:
        """
        Получение bounding box координат страны через Nominatim API

        Returns:
            Список [south, north, west, east] или None
        """
        headers = {
            'User-Agent': 'coursework-aeroplanes/1.0'
        }

        params = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        try:
            response = get(
                url=self.openstreetmap_url,
                params=params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data and len(data) > 0:
                boundingbox = data[0].get('boundingbox')
                if boundingbox:
                    return boundingbox  # [south, north, west, east]

        except Exception as e:
            print(f"Ошибка при получении координат страны {country}: {e}")

        return None

    def get_aeroplanes(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Получение информации о самолетах через OpenSky API

        Returns:
            Словарь с данными о самолетах
        """
        # Сначала получаем координаты страны
        bbox = self.get_country_coordinates(country)

        if not bbox:
            print(f"Не удалось найти координаты для страны: {country}")
            return None

        # Параметры для фильтрации по bounding box
        params = {
            'lamin': bbox[0],  # юг
            'lamax': bbox[1],  # север
            'lomin': bbox[2],  # запад
            'lomax': bbox[3],  # восток
        }

        try:
            response = get(
                url=self.opensky_url,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            self.last_response = response.json()
            return self.last_response

        except Exception as e:
            print(f"Ошибка при получении данных о самолетах: {e}")
            return None