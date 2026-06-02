import math
import sys

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QComboBox, QLabel,
                             QTextEdit, QProgressBar, QFileDialog, QSpinBox, QMessageBox)

from collisions import find_single_collision
from errors import FileUtilsError
from fileutils import save_json


class CalculationWorker(QThread):
    """Фоновый поток для поиска коллизий."""
    progress_update = pyqtSignal(int)
    calculation_finished = pyqtSignal(str, object)
    calculation_failed = pyqtSignal(str)

    def __init__(self, mode: str, bits: int, experiments: int = 100):
        super().__init__()
        self.mode = mode
        self.bits = bits
        self.experiments = experiments

    def run(self):
        try:
            if self.mode == "single":
                result = find_single_collision(self.bits)
                self.calculation_finished.emit("single", result)
            elif self.mode == "stats":
                attempts_list = []
                for i in range(self.experiments):
                    _, _, _, attempts = find_single_collision(self.bits)
                    attempts_list.append(attempts)
                    self.progress_update.emit(i + 1)
                self.calculation_finished.emit("stats", attempts_list)
        except Exception as e:
            self.calculation_failed.emit(str(e))


class HashCollisionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.saved_stats = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Поиск коллизий хеш-функций (Лабораторная №4)")
        self.resize(600, 450)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # --- Панель настроек ---
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Разрядность хеша:"))
        self.bits_combo = QComboBox()
        self.bits_combo.addItems(["8 бит", "12 бит", "16 бит"])
        settings_layout.addWidget(self.bits_combo)

        settings_layout.addWidget(QLabel("Кол-во экспериментов:"))
        self.exp_spinbox = QSpinBox()
        self.exp_spinbox.setRange(10, 5000)
        self.exp_spinbox.setValue(100)
        settings_layout.addWidget(self.exp_spinbox)
        main_layout.addLayout(settings_layout)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        self.btn_find = QPushButton("Найти 1 коллизию")
        self.btn_find.clicked.connect(self.run_single)
        btn_layout.addWidget(self.btn_find)

        self.btn_stats = QPushButton("Собрать статистику")
        self.btn_stats.clicked.connect(self.run_stats)
        btn_layout.addWidget(self.btn_stats)

        self.btn_save = QPushButton("Сохранить отчет...")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_report)
        btn_layout.addWidget(self.btn_save)
        main_layout.addLayout(btn_layout)

        # --- Прогресс-бар и лог ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("font-family: Consolas; font-size: 10pt;")
        main_layout.addWidget(self.log_area)

    def set_controls_enabled(self, state: bool):
        self.btn_find.setEnabled(state)
        self.btn_stats.setEnabled(state)
        self.bits_combo.setEnabled(state)
        self.exp_spinbox.setEnabled(state)

    def run_single(self):
        bits = int(self.bits_combo.currentText().split()[0])
        self.log_area.append(f"\n[*] Ищем коллизию ({bits} бит)... Пожалуйста, подождите.")
        self.progress_bar.setRange(0, 0)  # Анимация загрузки
        self.set_controls_enabled(False)

        self.worker = CalculationWorker("single", bits)
        self.worker.calculation_finished.connect(self.on_finished)
        self.worker.calculation_failed.connect(self.on_failed)
        self.worker.start()

    def run_stats(self):
        bits = int(self.bits_combo.currentText().split()[0])
        experiments = self.exp_spinbox.value()
        self.log_area.append(f"\n[*] Сбор статистики: {experiments} итераций ({bits} бит)...")
        self.progress_bar.setRange(0, experiments)
        self.progress_bar.setValue(0)
        self.set_controls_enabled(False)

        self.worker = CalculationWorker("stats", bits, experiments)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.calculation_finished.connect(self.on_finished)
        self.worker.calculation_failed.connect(self.on_failed)
        self.worker.start()

    def on_finished(self, mode: str, data):
        self.set_controls_enabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        if mode == "single":
            s1, s2, h_val, attempts = data
            self.log_area.append("[+] Коллизия найдена!")
            self.log_area.append(f" Строка 1 : {s1}")
            self.log_area.append(f" Строка 2 : {s2}")
            self.log_area.append(f" Хеш      : {h_val} (hex: {hex(h_val)})")
            self.log_area.append(f" Попыток  : {attempts}")

        elif mode == "stats":
            attempts_list = data
            avg_att = sum(attempts_list) / len(attempts_list)
            theoretical = 1.25 * math.sqrt(2 ** int(self.bits_combo.currentText().split()[0]))

            self.log_area.append("[+] Статистика собрана!")
            self.log_area.append(f" Минимум  : {min(attempts_list)}")
            self.log_area.append(f" Максимум : {max(attempts_list)}")
            self.log_area.append(f" Среднее  : {avg_att:.2f}")
            self.log_area.append(f" Ожидаемое: {theoretical:.2f}")

            self.saved_stats = {
                "bits": int(self.bits_combo.currentText().split()[0]),
                "experiments": len(attempts_list),
                "average": avg_att,
                "expected": theoretical,
                "raw_data": attempts_list
            }
            self.btn_save.setEnabled(True)

    def on_failed(self, error: str):
        self.set_controls_enabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "Ошибка", error)

    def save_report(self):
        if not self.saved_stats:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", "JSON (*.json)")
        if path:
            try:
                save_json(path, self.saved_stats)
                self.log_area.append(f"\n[OK] Отчет сохранен: {path}")
            except FileUtilsError as e:
                QMessageBox.critical(self, "Ошибка сохранения", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCollisionGUI()
    window.show()
    sys.exit(app.exec())
