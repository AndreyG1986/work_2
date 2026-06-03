# tests/test_base_saver.py
import unittest
from abc import ABC
from src.file_handlers.base_saver import BaseSaver
from src.models.aeroplane import Aeroplane


class TestBaseSaver(unittest.TestCase):

    def test_base_saver_is_abstract(self):
        """Тест: BaseSaver - абстрактный класс"""
        self.assertTrue(issubclass(BaseSaver, ABC))

    def test_base_saver_requires_implementation(self):
        """Тест: невозможно создать экземпляр абстрактного класса"""
        with self.assertRaises(TypeError):
            BaseSaver()  # Должен выбросить ошибку

    # Создаем конкретную реализацию для тестирования интерфейса
    class ConcreteSaver(BaseSaver):
        def add_aeroplane(self, aeroplane: Aeroplane) -> None:
            pass

        def get_aeroplanes(self, **filters):
            return []

        def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
            pass

        def delete_all(self) -> None:
            pass

    def test_concrete_saver_can_be_instantiated(self):
        """Тест: конкретную реализацию можно создать"""
        saver = self.ConcreteSaver()
        self.assertIsInstance(saver, BaseSaver)


if __name__ == "__main__":
    unittest.main()