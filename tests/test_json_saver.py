# tests/test_json_saver.py
import unittest
import json
import os
import tempfile
from src.file_handlers.json_saver import JSONSaver
from src.models.aeroplane import Aeroplane


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        """Создание временного файла для тестов"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_aeroplanes.json")
        self.saver = JSONSaver(self.test_file)

        self.test_planes = [
            Aeroplane("UAL1621", "United States", 268.79, 10203.18),
            Aeroplane("DLH431", "Germany", 250.00, 11000.00),
            Aeroplane("AFR123", "France", 245.50, 9500.00),
        ]

    def tearDown(self):
        """Удаление временных файлов"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_add_aeroplane(self):
        """Тест добавления одного самолета"""
        self.saver.add_aeroplane(self.test_planes[0])

        data = self.saver._load_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["callsign"], "UAL1621")

    def test_add_aeroplane_duplicate(self):
        """Тест добавления дубликата"""
        self.saver.add_aeroplane(self.test_planes[0])
        self.saver.add_aeroplane(self.test_planes[0])

        data = self.saver._load_data()
        self.assertEqual(len(data), 1)  # Дубликат не добавился

    def test_add_aeroplanes_batch(self):
        """Тест пакетного добавления самолетов"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        data = self.saver._load_data()
        self.assertEqual(len(data), 3)

    def test_add_aeroplanes_batch_with_existing(self):
        """Тест пакетного добавления с существующими данными"""
        # Добавляем первый самолет
        self.saver.add_aeroplane(self.test_planes[0])

        # Пакетно добавляем все три
        self.saver.add_aeroplanes_batch(self.test_planes)

        data = self.saver._load_data()
        # Должно быть 3 (первый не дублируется)
        self.assertEqual(len(data), 3)

    def test_add_aeroplanes_batch_empty(self):
        """Тест пакетного добавления пустого списка"""
        self.saver.add_aeroplanes_batch([])
        data = self.saver._load_data()
        self.assertEqual(len(data), 0)

    def test_get_aeroplanes_no_filters(self):
        """Тест получения всех самолетов без фильтров"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        result = self.saver.get_aeroplanes()
        self.assertEqual(len(result), 3)

    def test_get_aeroplanes_filter_by_country(self):
        """Тест фильтрации по стране"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        result = self.saver.get_aeroplanes(origin_country="Germany")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "DLH431")

    def test_get_aeroplanes_filter_by_altitude_range(self):
        """Тест фильтрации по диапазону высот"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        result = self.saver.get_aeroplanes(min_altitude=10000, max_altitude=12000)
        self.assertEqual(len(result), 2)  # UAL1621 и DLH431

    def test_get_aeroplanes_filter_by_min_altitude_only(self):
        """Тест фильтрации по минимальной высоте"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        result = self.saver.get_aeroplanes(min_altitude=10000)
        self.assertEqual(len(result), 2)

    def test_get_aeroplanes_filter_by_max_altitude_only(self):
        """Тест фильтрации по максимальной высоте"""
        self.saver.add_aeroplanes_batch(self.test_planes)

        result = self.saver.get_aeroplanes(max_altitude=10000)
        self.assertEqual(len(result), 1)  # Только AFR123

    def test_delete_aeroplane(self):
        """Тест удаления самолета"""
        self.saver.add_aeroplanes_batch(self.test_planes)
        self.saver.delete_aeroplane(self.test_planes[0])

        data = self.saver._load_data()
        self.assertEqual(len(data), 2)
        callsigns = [item["callsign"] for item in data]
        self.assertNotIn("UAL1621", callsigns)

    def test_delete_aeroplane_not_exists(self):
        """Тест удаления несуществующего самолета"""
        self.saver.add_aeroplanes_batch(self.test_planes)
        new_plane = Aeroplane("TEST", "Test", 100, 5000)
        self.saver.delete_aeroplane(new_plane)

        data = self.saver._load_data()
        self.assertEqual(len(data), 3)  # Количество не изменилось

    def test_delete_all(self):
        """Тест удаления всех данных"""
        self.saver.add_aeroplanes_batch(self.test_planes)
        self.saver.delete_all()

        data = self.saver._load_data()
        self.assertEqual(len(data), 0)

    def test_load_data_from_nonexistent_file(self):
        """Тест загрузки из несуществующего файла"""
        data = self.saver._load_data()
        self.assertEqual(data, [])

    def test_save_and_load_empty_data(self):
        """Тест сохранения и загрузки пустых данных"""
        self.saver.delete_all()
        data = self.saver._load_data()
        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
