# src/file_handlers/json_saver.py
import json
import os
from typing import List, Optional
from src.file_handlers.base_saver import BaseSaver
from src.models.aeroplane import Aeroplane


class JSONSaver(BaseSaver):
    """Класс для сохранения информации о самолетах в JSON-файл"""

    def __init__(self, filepath: str = "data/aeroplanes.json"):
        self.filepath = filepath
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Создание директории для файла, если её нет"""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _load_data(self) -> List[dict]:
        """Загрузка данных из JSON файла"""
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[dict]) -> None:
        """Сохранение данных в JSON файл"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавление самолета в файл (оптимизированная версия)"""
        # Пропускаем дубликаты по позывному
        data = self._load_data()
        aeroplane_dict = aeroplane.to_dict()

        # Проверяем, есть ли уже такой самолет по позывному
        exists = any(item.get("callsign") == aeroplane_dict.get("callsign") for item in data)
        if not exists:
            data.append(aeroplane_dict)
            self._save_data(data)

    def add_aeroplanes_batch(self, aeroplanes: List[Aeroplane]) -> None:
        """
        Пакетное добавление самолетов (оптимизировано для большого количества)
        """
        if not aeroplanes:
            return

        # Загружаем существующие данные
        existing_data = self._load_data()
        existing_callsigns = {item.get("callsign") for item in existing_data}

        # Добавляем только новые самолеты
        new_aeroplanes = []
        for aeroplane in aeroplanes:
            if aeroplane.callsign not in existing_callsigns:
                new_aeroplanes.append(aeroplane.to_dict())
                existing_callsigns.add(aeroplane.callsign)

        if new_aeroplanes:
            existing_data.extend(new_aeroplanes)
            self._save_data(existing_data)
            print(f"  ✅ Добавлено {len(new_aeroplanes)} новых самолетов")
        else:
            print(f"  ℹ️ Нет новых самолетов для добавления")

    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """
        Получение самолетов по фильтрам

        Filters:
            origin_country: фильтр по стране регистрации
            min_altitude: минимальная высота
            max_altitude: максимальная высота
        """
        data = self._load_data()
        aeroplanes = []

        for item in data:
            # Применяем фильтры
            if "origin_country" in filters:
                if item["origin_country"] != filters["origin_country"]:
                    continue

            if "min_altitude" in filters:
                if item["altitude"] < filters["min_altitude"]:
                    continue

            if "max_altitude" in filters:
                if item["altitude"] > filters["max_altitude"]:
                    continue

            try:
                aeroplane = Aeroplane(
                    callsign=item["callsign"],
                    origin_country=item["origin_country"],
                    velocity=item["velocity"],
                    altitude=item["altitude"],
                    longitude=item.get("longitude"),
                    latitude=item.get("latitude"),
                    on_ground=item.get("on_ground"),
                )
                aeroplanes.append(aeroplane)
            except ValueError:
                continue

        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаление самолета из файла"""
        data = self._load_data()
        aeroplane_dict = aeroplane.to_dict()

        if aeroplane_dict in data:
            data.remove(aeroplane_dict)
            self._save_data(data)

    def delete_all(self) -> None:
        """Удаление всех данных"""
        self._save_data([])
