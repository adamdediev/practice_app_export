"""
Бизнес-логика модуля «АРМ руководителя производственной практики».

Здесь сосредоточена ВСЯ логика расчётов и валидации.
Интерфейс (app.py) не содержит вычислений — только ввод/вывод.
Такое разделение соответствует принципу Single Responsibility (SRP) из SOLID.
"""

from typing import List


class ArgumentOutOfRangeException(Exception):
    """
    Исключение, выбрасываемое при выходе оценки за допустимый диапазон [2..5].

    В C#/Java существует штатный класс с таким именем; в Python его нет,
    поэтому объявляем собственный — так требование ТЗ (Тест 3) выполняется буквально.
    """
    pass


class PracticeRecord:
    """Запись о прохождении практики одним студентом."""

    MIN_GRADE = 2
    MAX_GRADE = 5

    def __init__(self, fio: str, group: str, grades: List[int]):
        # Используем сеттеры, чтобы валидация сработала уже в конструкторе.
        self.set_fio(fio)
        self.set_group(group)
        self.set_grades(grades)

    # ----------------------- Геттеры -----------------------
    def get_fio(self) -> str:
        return self.__fio

    def get_group(self) -> str:
        return self.__group

    def get_grades(self) -> List[int]:
        # Возвращаем копию, чтобы извне нельзя было изменить приватный список.
        return list(self.__grades)

    # ----------------------- Сеттеры с валидацией -----------------------
    def set_fio(self, fio: str) -> None:
        if fio is None or str(fio).strip() == "":
            raise ValueError("Поле «ФИО» не может быть пустым.")
        self.__fio = str(fio).strip()

    def set_group(self, group: str) -> None:
        if group is None or str(group).strip() == "":
            raise ValueError("Поле «Группа» не может быть пустым.")
        self.__group = str(group).strip()

    def set_grades(self, grades: List[int]) -> None:
        if grades is None or len(grades) != 3:
            raise ValueError("Необходимо указать ровно три оценки.")
        validated = []
        for raw in grades:
            validated.append(self.__validate_grade(raw))
        self.__grades = validated

    # ----------------------- Внутренняя валидация одной оценки -----------------------
    @staticmethod
    def __validate_grade(raw) -> int:
        # Запрет текста/спецсимволов: пытаемся привести к целому числу.
        try:
            # bool — подкласс int, отсекаем его отдельно, чтобы True не стал 1.
            if isinstance(raw, bool):
                raise ValueError
            grade = int(raw)
        except (ValueError, TypeError):
            raise ValueError("Ошибка: Оценка должна быть числом от 2 до 5.")

        # Проверка диапазона.
        if grade < PracticeRecord.MIN_GRADE or grade > PracticeRecord.MAX_GRADE:
            raise ArgumentOutOfRangeException(
                f"Ошибка: Оценка {grade} вне диапазона. Допустимы целые числа от 2 до 5."
            )
        return grade

    # ----------------------- Бизнес-методы -----------------------
    def calculate_average(self) -> float:
        """Средний балл, округлённый до одного знака после запятой."""
        return round(sum(self.__grades) / len(self.__grades), 1)

    def determine_status(self) -> str:
        """
        Определение статуса допуска.

        Бизнес-правило: если ХОТЯ БЫ ОДНА оценка равна 2 — «Не допущен»,
        независимо от среднего балла. Иначе — «Допущен к аттестации».
        """
        for grade in self.__grades:
            if grade == 2:
                return "Не допущен"
        return "Допущен к аттестации"

    def is_admitted(self) -> bool:
        return self.determine_status() == "Допущен к аттестации"

    def __repr__(self) -> str:
        return (f"PracticeRecord(fio='{self.__fio}', group='{self.__group}', "
                f"grades={self.__grades}, avg={self.calculate_average()}, "
                f"status='{self.determine_status()}')")
