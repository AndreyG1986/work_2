from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Aeroplane:
    """Класс для представления информации о самолете"""

    callsign: str  # Позывной (ICAO24)
    origin_country: str  # Страна регистрации
    velocity: float  # Скорость (м/с)
    altitude: float  # Высота (м)
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    on_ground: Optional[bool] = None

    def __post_init__(self):
        """Валидация данных после инициализации"""
        self._validate_callsign()
        self._validate_country()
        self._validate_velocity()
        self._validate_altitude()

    def _validate_callsign(self):
        """Валидация позывного"""
        if not self.callsign or not isinstance(self.callsign, str):
            raise ValueError("Позывной должен быть непустой строкой")

    def _validate_country(self):
        """Валидация страны регистрации"""
        if not self.origin_country or not isinstance(self.origin_country, str):
            raise ValueError("Страна регистрации должна быть непустой строкой")

    def _validate_velocity(self):
        """Валидация скорости"""
        if not isinstance(self.velocity, (int, float)):
            raise ValueError("Скорость должна быть числом")
        if self.velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")

    def _validate_altitude(self):
        """Валидация высоты"""
        if not isinstance(self.altitude, (int, float)):
            raise ValueError("Высота должна быть числом")
        # Высота может быть None или отрицательной (под землей)

    def __lt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте (для сортировки)"""
        return self.altitude < other.altitude

    def __gt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте (для сортировки)"""
        return self.altitude > other.altitude

    def __eq__(self, other: 'Aeroplane') -> bool:
        """Сравнение по позывному"""
        return self.callsign == other.callsign

    @classmethod
    def from_api_state(cls, state: List) -> Optional['Aeroplane']:
        """
        Создание объекта самолета из данных OpenSky API

        Формат state:
        [
            icao24, callsign, origin_country, time_position,
            last_contact, longitude, latitude, baro_altitude,
            on_ground, velocity, true_track, vertical_rate,
            sensors, geo_altitude, squawk, spi, position_source
        ]
        """
        if not state or len(state) < 10:
            return None

        # Извлекаем нужные поля
        icao24 = state[0]
        callsign = (state[1] or "N/A").strip()
        origin_country = state[2] or "Unknown"
        longitude = state[5]
        latitude = state[6]
        altitude = state[9] if state[9] is not None else 0  # baro_altitude
        velocity = state[10] if state[10] is not None else 0
        on_ground = state[8] if state[8] is not None else False

        try:
            return cls(
                callsign=callsign,
                origin_country=origin_country,
                velocity=float(velocity),
                altitude=float(altitude),
                longitude=float(longitude) if longitude else None,
                latitude=float(latitude) if latitude else None,
                on_ground=bool(on_ground)
            )
        except (ValueError, TypeError):
            return None

    @classmethod
    def cast_to_object_list(cls, api_response: Dict[str, Any]) -> List['Aeroplane']:
        """
        Преобразование ответа API в список объектов Aeroplane
        """
        aeroplanes = []

        if not api_response or 'states' not in api_response:
            return aeroplanes

        states = api_response['states']
        if not states:
            return aeroplanes

        for state in states:
            aeroplane = cls.from_api_state(state)
            if aeroplane:
                aeroplanes.append(aeroplane)

        return aeroplanes

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта в словарь для сохранения"""
        return {
            'callsign': self.callsign,
            'origin_country': self.origin_country,
            'velocity': self.velocity,
            'altitude': self.altitude,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'on_ground': self.on_ground
        }