import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QLabel, QLineEdit, QMessageBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)

from analysis_utils import diff_percent, count_bit_diff
from hash_utils import compute_hash
from mutation_utils import apply_mutation


class HashApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исследование лавинного эффекта хеш-функций")

        self.resize(1280, 720)

        try:
            self.settings = self.load_settings()
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", str(e))
            sys.exit(1)

        self.algorithms = self.settings.get("algorithms", {})

        if not self.algorithms:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить алгоритмы")
            sys.exit(1)

        self.results = {}
        self.original_text = ""
        self.original_hash = ""

        self.init_ui()

    def load_settings(self):
        """
        Загрузка настроек из JSON файла.

        Returns:
            Словарь с настройками приложения.
        """
        if not os.path.exists("settings.json"):
            raise FileNotFoundError("settings.json не найден")

        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Ошибка чтения settings.json: {e}")

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите строку")
        layout.addWidget(self.input_field)

        self.algo_box = QComboBox()
        self.algo_box.addItems(self.algorithms.keys())
        self.algo_box.currentIndexChanged.connect(self.reset_state)
        layout.addWidget(QLabel("Алгоритм:"))
        layout.addWidget(self.algo_box)

        self.hash_label = QLabel("Хеш:")
        self.hash_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.hash_label)

        btn_hash = QPushButton("Вычислить хеш")
        btn_hash.clicked.connect(self.compute_hash)
        layout.addWidget(btn_hash)

        btn_char = QPushButton("Изменить символ")
        btn_char.clicked.connect(lambda: self.run_experiment("char"))
        layout.addWidget(btn_char)

        btn_bit = QPushButton("Изменить бит")
        btn_bit.clicked.connect(lambda: self.run_experiment("bit"))
        layout.addWidget(btn_bit)

        btn_reg = QPushButton("Изменить регистр")
        btn_reg.clicked.connect(lambda: self.run_experiment("reg"))
        layout.addWidget(btn_reg)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "Операция", "Изменённые биты", "% различий", "Новый хеш"
        ])
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(3, 1024)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def reset_state(self):
        self.original_text = ""
        self.original_hash = ""
        self.hash_label.setText("Хеш:")
        self.table.setRowCount(0)

    def current_algo(self):
        """
        Получение выбранного в данный момент алгоритма хеширования.

        Returns:
            Кортеж (название_алгоритма, системный_идентификатор).
        """
        algo_name = self.algo_box.currentText()
        return algo_name, self.algorithms[algo_name]

    def compute_hash(self):
        try:
            text = self.input_field.text()

            if not text:
                raise ValueError("Введите строку")

            name, algo = self.current_algo()

            self.original_text = text
            self.original_hash = compute_hash(text, algo)

            self.hash_label.setText(f"{name}: {self.original_hash}")

            self.table.setRowCount(0)

            if name not in self.results:
                self.results[name] = []

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def run_experiment(self, mode: str):
        """
        Проведение одного эксперимента по мутации строки и расчет лавинного эффекта.

        Args:
            mode: Режим мутации ("char", "bit" или "reg").
        """
        try:
            if not self.original_text:
                raise ValueError("Сначала вычислите хеш")

            name, algo = self.current_algo()

            new_bytes, op = apply_mutation(self.original_text, mode)

            new_hash = compute_hash(new_bytes, algo)

            total_bits = len(self.original_hash) * 4
            diff = count_bit_diff(self.original_hash, new_hash)
            percent = diff_percent(diff, total_bits)

            row = {
                "Операция": op,
                "Новый хеш": new_hash,
                "Diff bits": diff,
                "%": percent
            }

            self.results[name].append(row)
            self.add_to_table(row)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_to_table(self, row):
        r = self.table.rowCount()
        self.table.insertRow(r)

        self.table.setItem(r, 0, QTableWidgetItem(row["Операция"]))
        self.table.setItem(r, 1, QTableWidgetItem(str(row["Diff bits"])))
        self.table.setItem(r, 2, QTableWidgetItem(f"{row['%']:.2f}%"))
        self.table.setItem(r, 3, QTableWidgetItem(row["Новый хеш"]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HashApp()
    window.show()
    sys.exit(app.exec_())
