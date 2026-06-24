"""
Графический интерфейс (UI) модуля «АРМ руководителя производственной практики».

Слой представления. Никаких расчётов здесь нет — вся логика делегируется
классу PracticeRecord. Это разделение ответственности (SRP / SOLID):
UI можно заменить (web, консоль), а бизнес-логика останется неизменной.

Запуск:  python app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from practice_record import PracticeRecord, ArgumentOutOfRangeException



class PracticeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("АРМ руководителя производственной практики")
        self.geometry("520x430")
        self.resizable(False, False)
        self.configure(bg="#f0f2f5")
        self._build_ui()

    # ----------------------- Построение интерфейса -----------------------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        header = tk.Label(self, text="Учёт результатов производственной практики",
                          font=("Segoe UI", 13, "bold"), bg="#f0f2f5", fg="#1a1a1a")
        header.grid(row=0, column=0, columnspan=2, pady=(14, 10))

        # --- ФИО ---
        tk.Label(self, text="ФИО студента:", bg="#f0f2f5",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", **pad)
        self.entry_fio = tk.Entry(self, width=32, font=("Segoe UI", 10))
        self.entry_fio.grid(row=1, column=1, sticky="w", **pad)

        # --- Группа ---
        tk.Label(self, text="Группа:", bg="#f0f2f5",
                 font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", **pad)
        self.entry_group = tk.Entry(self, width=32, font=("Segoe UI", 10))
        self.entry_group.grid(row=2, column=1, sticky="w", **pad)

        # --- Оценки (выпадающие списки 2..5, плюс пустое значение для демонстрации ошибок) ---
        grade_values = ["", "2", "3", "4", "5"]

        tk.Label(self, text="Оценка за дневник:", bg="#f0f2f5",
                 font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", **pad)
        self.cb_diary = ttk.Combobox(self, values=grade_values, width=29, font=("Segoe UI", 10))
        self.cb_diary.grid(row=3, column=1, sticky="w", **pad)

        tk.Label(self, text="Оценка за задание:", bg="#f0f2f5",
                 font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", **pad)
        self.cb_task = ttk.Combobox(self, values=grade_values, width=29, font=("Segoe UI", 10))
        self.cb_task.grid(row=4, column=1, sticky="w", **pad)

        tk.Label(self, text="Оценка за отчёт:", bg="#f0f2f5",
                 font=("Segoe UI", 10)).grid(row=5, column=0, sticky="w", **pad)
        self.cb_report = ttk.Combobox(self, values=grade_values, width=29, font=("Segoe UI", 10))
        self.cb_report.grid(row=5, column=1, sticky="w", **pad)

        # --- Кнопка расчёта ---
        btn = tk.Button(self, text="Рассчитать результат", command=self.on_calculate,
                        bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"),
                        activebackground="#1d4ed8", activeforeground="white",
                        relief="flat", cursor="hand2", padx=10, pady=6)
        btn.grid(row=6, column=0, columnspan=2, pady=14)

        # --- Информационная панель результата ---
        self.result_panel = tk.Label(self, text="Введите данные и нажмите «Рассчитать»",
                                      font=("Segoe UI", 11, "bold"), bg="#e5e7eb",
                                      fg="#374151", width=46, height=3, wraplength=420,
                                      justify="center")
        self.result_panel.grid(row=7, column=0, columnspan=2, padx=12, pady=8)

    # ----------------------- Обработчик кнопки -----------------------
    def on_calculate(self):
        """
        Перехватывает все нарушения валидации через try-except,
        чтобы приложение не завершалось аварийно (требование надёжности ТЗ).
        """
        try:
            fio = self.entry_fio.get()
            group = self.entry_group.get()
            grades = [
                self._parse_grade(self.cb_diary.get(), "дневник"),
                self._parse_grade(self.cb_task.get(), "задание"),
                self._parse_grade(self.cb_report.get(), "отчёт"),
            ]

            record = PracticeRecord(fio, group, grades)
            average = record.calculate_average()
            status = record.determine_status()

            self._show_result(record.get_fio(), average, status, record.is_admitted())

        except ArgumentOutOfRangeException as e:
            messagebox.showerror("Ошибка диапазона", str(e))
            self._reset_panel()
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            self._reset_panel()
        except Exception as e:
            # Страховочный перехват любых непредвиденных ошибок.
            messagebox.showerror("Непредвиденная ошибка", f"Произошла ошибка: {e}")
            self._reset_panel()

    @staticmethod
    def _parse_grade(value: str, field_name: str):
        """Пустое поле оценки = осмысленная ошибка, а не падение приложения."""
        if value is None or str(value).strip() == "":
            raise ValueError(f"Ошибка: не указана оценка за «{field_name}».")
        return value  # дальнейшую валидацию (число/диапазон) выполнит PracticeRecord

    # ----------------------- Вывод результата с цветом -----------------------
    def _show_result(self, fio, average, status, admitted):
        color_bg = "#dcfce7" if admitted else "#fee2e2"   # зелёный / красный фон
        color_fg = "#166534" if admitted else "#991b1b"   # тёмно-зелёный / тёмно-красный текст
        text = f"{fio}\nСредний балл: {average}\nСтатус: {status}"
        self.result_panel.config(text=text, bg=color_bg, fg=color_fg)

    def _reset_panel(self):
        self.result_panel.config(text="Исправьте ошибку и повторите расчёт",
                                 bg="#e5e7eb", fg="#374151")


if __name__ == "__main__":
    app = PracticeApp()
    app.mainloop()
