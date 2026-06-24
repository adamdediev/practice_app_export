"""
Модульные тесты бизнес-логики (unittest).

Покрывают сценарии из ТЗ:
  Тест 1 — успешный допуск (4, 4, 5)
  Тест 2 — недопуск из-за двойки (5, 5, 2)
  Тест 3 — исключение ArgumentOutOfRangeException при оценке 6
плюс дополнительные граничные случаи.

Запуск:  python -m unittest discover -s tests -v
"""

import unittest
import sys
import os

# Чтобы тесты находили модуль из корня проекта.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from practice_record import PracticeRecord, ArgumentOutOfRangeException


class TestDetermineStatus(unittest.TestCase):

    # --- Тест 1: успешный допуск ---
    def test_admission_success(self):
        record = PracticeRecord("Иванов И.И.", "ИС-41", [4, 4, 5])
        self.assertEqual(record.determine_status(), "Допущен к аттестации")
        self.assertTrue(record.is_admitted())

    # --- Тест 2: недопуск из-за двойки ---
    def test_not_admitted_due_to_two(self):
        record = PracticeRecord("Петров П.П.", "ИС-41", [5, 5, 2])
        self.assertEqual(record.determine_status(), "Не допущен")
        self.assertFalse(record.is_admitted())

    # --- Тест 3: исключение при оценке вне диапазона ---
    def test_grade_out_of_range_raises(self):
        with self.assertRaises(ArgumentOutOfRangeException):
            PracticeRecord("Сидоров С.С.", "ИС-41", [6, 4, 5])

    # --- Дополнительно: расчёт среднего балла ---
    def test_calculate_average_rounding(self):
        record = PracticeRecord("Кузнецов К.К.", "ИС-42", [5, 4, 4])
        self.assertEqual(record.calculate_average(), 4.3)  # 13/3 = 4.333 -> 4.3

    # --- Дополнительно: все пятёрки ---
    def test_all_fives_admitted(self):
        record = PracticeRecord("Смирнова А.А.", "ИС-42", [5, 5, 5])
        self.assertEqual(record.determine_status(), "Допущен к аттестации")
        self.assertEqual(record.calculate_average(), 5.0)

    # --- Дополнительно: текст вместо оценки ---
    def test_text_grade_raises_value_error(self):
        with self.assertRaises(ValueError):
            PracticeRecord("Тест Т.Т.", "ИС-42", ["пять", 4, 5])

    # --- Дополнительно: пустое ФИО ---
    def test_empty_fio_raises(self):
        with self.assertRaises(ValueError):
            PracticeRecord("   ", "ИС-42", [4, 4, 4])

    # --- Дополнительно: инкапсуляция (нельзя изменить список снаружи) ---
    def test_encapsulation_grades_copy(self):
        record = PracticeRecord("Ост И.О.", "ИС-42", [3, 3, 3])
        grades = record.get_grades()
        grades[0] = 99
        self.assertEqual(record.get_grades(), [3, 3, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
