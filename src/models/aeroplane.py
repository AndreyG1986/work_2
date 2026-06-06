# src/models/aeroplane.py
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
        # Разрешаем пустые позывные, заменяя их на "N/A"
        if not self.callsign or not isinstance(self.callsign, str):
            self.callsign = "N/A"
        elif self.callsign.strip() == "":
            self.callsign = "N/A"

    def _validate_country(self):
        """Валидация страны регистрации"""
        if not self.origin_country or not isinstance(self.origin_country, str):
            self.origin_country = "Unknown"
        elif self.origin_country.strip() == "":
            self.origin_country = "Unknown"

    def _validate_velocity(self):
        """Валидация скорости"""
        if not isinstance(self.velocity, (int, float)):
            self.velocity = 0.0
        if self.velocity < 0:
            self.velocity = 0.0

    def _validate_altitude(self):
        """Валидация высоты"""
        if not isinstance(self.altitude, (int, float)):
            self.altitude = 0.0
        # Высота может быть отрицательной (под землей), оставляем как есть

    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (для сортировки)"""
        return self.altitude < other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнение по высоте (для сортировки)"""
        return self.altitude > other.altitude

    def __eq__(self, other: "Aeroplane") -> bool:
        """Сравнение по позывному"""
        return self.callsign == other.callsign

    @classmethod
    def from_api_state(cls, state: List) -> Optional["Aeroplane"]:
        """
        Создание объекта самолета из данных OpenSky API

        Индексы массива state (согласно документации OpenSky):
        0: icao24,        1: callsign,       2: origin_country,
        3: time_position, 4: last_contact,   5: longitude,
        6: latitude,      7: baro_altitude,  8: on_ground,
        9: velocity,      10: true_track,    11: vertical_rate,
        12: sensors,      13: geo_altitude,  14: squawk,
        15: spi,          16: position_source
        """
        if not state or len(state) < 10:
            return None

        # Извлекаем поля с правильными индексами
        # Обрабатываем callsign - он может быть None или пустым
        callsign_raw = state[1]
        if callsign_raw is None or str(callsign_raw).strip() == "":
            callsign = "N/A"
        else:
            callsign = str(callsign_raw).strip()

        origin_country = state[2] if state[2] else "Unknown"
        longitude = state[5]
        latitude = state[6]

        # Высота: сначала пробуем baro_altitude (индекс 7), затем geo_altitude (индекс 13)
        altitude = state[7] if state[7] is not None else (state[13] if state[13] is not None else 0.0)

        # Статус на земле (индекс 8)
        on_ground = state[8] if state[8] is not None else False

        # Скорость (индекс 9)
        velocity = state[9] if state[9] is not None else 0.0

        try:
            return cls(
                callsign=callsign,
                origin_country=origin_country,
                velocity=float(velocity),
                altitude=float(altitude),
                longitude=float(longitude) if longitude is not None else None,
                latitude=float(latitude) if latitude is not None else None,
                on_ground=bool(on_ground),
            )
        except (ValueError, TypeError) as e:
            # Тихая обработка ошибки, возвращаем None
            return None

    @classmethod
    def cast_to_object_list(cls, api_response: Dict[str, Any]) -> List["Aeroplane"]:
        """
        Преобразование ответа API в список объектов Aeroplane
        """
        aeroplanes = []

        if not api_response or "states" not in api_response:
            return aeroplanes

        states = api_response["states"]
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
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "on_ground": self.on_ground,
        }
