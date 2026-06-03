# src/api/aeroplanes_api.py
from typing import Dict, Any, Optional, List
from requests import get, Timeout
from src.api.base_api import BaseAPI


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API сервисов Nominatim и OpenSky"""

    def __init__(self, timeout: int = 60):
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api/states/all'
        self.timeout = timeout
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
            print(f"  📡 Получение координат страны {country}...")
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
                    print(f"  ✅ Координаты получены: {boundingbox}")
                    return boundingbox  # [south, north, west, east]

        except Timeout:
            print(f"  ❌ Таймаут при получении координат страны {country}")
        except Exception as e:
            print(f"  ❌ Ошибка при получении координат страны {country}: {e}")

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
            print(f"❌ Не удалось найти координаты для страны: {country}")
            return None

        # Параметры для фильтрации по bounding box
        params = {
            'lamin': bbox[0],  # юг
            'lamax': bbox[1],  # север
            'lomin': bbox[2],  # запад
            'lomax': bbox[3],  # восток
        }

        print(f"  📡 Запрос данных о самолетах в области...")
        print(f"     Юг: {bbox[0]}, Север: {bbox[1]}")
        print(f"     Запад: {bbox[2]}, Восток: {bbox[3]}")

        try:
            response = get(
                url=self.opensky_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            self.last_response = response.json()

            # Выводим информацию о полученных данных
            if self.last_response and 'states' in self.last_response:
                states_count = len(self.last_response['states']) if self.last_response['states'] else 0
                print(f"  ✅ Получено {states_count} записей о самолетах")

            return self.last_response

        except Timeout:
            print(f"  ❌ Таймаут при получении данных о самолетах (>{self.timeout} сек)")
            return None
        except Exception as e:
            print(f"  ❌ Ошибка при получении данных о самолетах: {e}")
            return None