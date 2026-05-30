import sys
from typing import Optional, Dict
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox, QTextEdit, QGroupBox,
    QTableWidget, QTableWidgetItem, QProgressBar, QMessageBox, QTabWidget
)
from PyQt5.QtCore import QThread, pyqtSignal
from attack import find_collision, get_expected_attempts
from hash_utils import get_hash, compute_full_hash

class AttackThread(QThread):
    """Поток для выполнения поиска коллизии без блокировки основного интерфейса."""
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object, object, object)
    error = pyqtSignal(str)

    def __init__(self, bits: int, max_attempts: int):
        super().__init__()
        self.bits = bits
        self.max_attempts = max_attempts

    def run(self):
        try:
            str1, str2, attempts, hash_table = find_collision(self.bits, self.max_attempts)
            self.finished.emit(str1, str2, attempts, hash_table)
        except Exception as e:
            self.error.emit(str(e))

class ExperimentsThread(QThread):
    """Поток для выполнения серии экспериментов в фоновом режиме."""
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(list, int)
    error = pyqtSignal(str)

    def __init__(self, bits: int, count: int, max_attempts: int):
        super().__init__()
        self.bits = bits
        self.count = count
        self.max_attempts = max_attempts

    def run(self):
        try:
            results = []
            for i in range(self.count):
                self.progress.emit(i + 1, self.count)
                str1, str2, attempts, _ = find_collision(self.bits, self.max_attempts)
                match (str1 is not None, str2 is not None):
                    case (True, True):
                        results.append((i + 1, str1[:50], str2[:50], attempts))
                    case _:
                        results.append((i + 1, "—", "—", f">{self.max_attempts}"))
            self.finished.emit(results, self.bits)
        except Exception as e:
            self.error.emit(str(e))

class BirthdayAttackGUI(QMainWindow):
    """Главное окно приложения для демонстрации атаки «Парадокс дней рождения»."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Атака «Парадокс дней рождения»")
        self.setMinimumSize(900, 600)
        self.attack_thread: Optional[AttackThread] = None
        self.experiments_thread: Optional[ExperimentsThread] = None
        self.init_ui()

    def init_ui(self) -> None:
        """Инициализирует пользовательский интерфейс приложения."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        attack_tab = self.create_attack_tab()
        tabs.addTab(attack_tab, "Поиск коллизии")

        experiments_tab = self.create_experiments_tab()
        tabs.addTab(experiments_tab, "Серия экспериментов")

    def create_attack_tab(self) -> QWidget:
        """Создаёт и настраивает вкладку для поиска одной коллизии."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        settings_group = QGroupBox("Настройки")
        settings_layout = QHBoxLayout(settings_group)

        settings_layout.addWidget(QLabel("Длина хеша (бит):"))
        self.hash_size_combo = QComboBox()
        self.hash_size_combo.addItems(["8", "12", "16"])
        settings_layout.addWidget(self.hash_size_combo)

        settings_layout.addWidget(QLabel("Макс. попыток:"))
        self.max_attempts_spin = QSpinBox()
        self.max_attempts_spin.setRange(1000, 1000000)
        self.max_attempts_spin.setValue(100000)
        self.max_attempts_spin.setSingleStep(10000)
        settings_layout.addWidget(self.max_attempts_spin)

        self.attack_btn = QPushButton("Найти коллизию")
        settings_layout.addWidget(self.attack_btn)
        layout.addWidget(settings_group)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        results_group = QGroupBox("Результаты")
        results_layout = QVBoxLayout(results_group)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        layout.addWidget(results_group)

        self.attack_btn.clicked.connect(self.start_attack)
        return tab

    def create_experiments_tab(self) -> QWidget:
        """Создаёт и настраивает вкладку для запуска серии экспериментов."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        settings_group = QGroupBox("Настройки эксперимента")
        settings_layout = QHBoxLayout(settings_group)

        settings_layout.addWidget(QLabel("Длина хеша (бит):"))
        self.exp_hash_combo = QComboBox()
        self.exp_hash_combo.addItems(["8", "12", "16"])
        settings_layout.addWidget(self.exp_hash_combo)

        settings_layout.addWidget(QLabel("Кол-во экспериментов:"))
        self.exp_count_spin = QSpinBox()
        self.exp_count_spin.setRange(1, 20)
        self.exp_count_spin.setValue(5)
        settings_layout.addWidget(self.exp_count_spin)

        settings_layout.addWidget(QLabel("Макс. попыток:"))
        self.exp_max_attempts_spin = QSpinBox()
        self.exp_max_attempts_spin.setRange(1000, 1000000)
        self.exp_max_attempts_spin.setValue(50000)
        self.exp_max_attempts_spin.setSingleStep(10000)
        settings_layout.addWidget(self.exp_max_attempts_spin)

        self.exp_btn = QPushButton("Запустить эксперименты")
        settings_layout.addWidget(self.exp_btn)
        layout.addWidget(settings_group)

        self.exp_progress_bar = QProgressBar()
        layout.addWidget(self.exp_progress_bar)

        self.exp_table = QTableWidget()
        self.exp_table.setColumnCount(4)
        self.exp_table.setHorizontalHeaderLabels(["№", "Строка 1", "Строка 2", "Попыток"])
        self.exp_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.exp_table)

        self.exp_btn.clicked.connect(self.start_experiments)
        return tab

    def start_attack(self) -> None:
        """Запускает поиск коллизии в отдельном потоке."""
        try:
            bits = int(self.hash_size_combo.currentText())
            max_attempts = self.max_attempts_spin.value()

            self.attack_btn.setEnabled(False)
            self.progress_bar.setMaximum(max_attempts)
            self.progress_bar.setValue(0)
            self.results_text.clear()

            self.attack_thread = AttackThread(bits, max_attempts)
            self.attack_thread.progress.connect(self.update_progress)
            self.attack_thread.finished.connect(self.on_attack_finished)
            self.attack_thread.error.connect(self.on_attack_error)
            self.attack_thread.start()
        except Exception as e:
            self.on_attack_error(str(e))

    def update_progress(self, current: int, total: int) -> None:
        """Обновляет индикатор прогресса выполнения."""
        self.progress_bar.setValue(current)

    def on_attack_finished(self, str1: Optional[str], str2: Optional[str], attempts: int, hash_table: Dict) -> None:
        """Обрабатывает успешное завершение поиска коллизии."""
        try:
            bits = int(self.hash_size_combo.currentText())
            match (str1 is not None, str2 is not None):
                case (True, True):
                    expected = get_expected_attempts(bits)
                    self.results_text.append("Коллизия найдена!\n")
                    self.results_text.append("Статистика:")
                    self.results_text.append(f"Длина хеша: {bits} бит")
                    self.results_text.append(f"Попыток: {attempts}")
                    self.results_text.append(f"Ожидаемое количество попыток (теория): ~{expected}")
                    self.results_text.append(f"Эффективность: {expected / attempts * 100:.1f}% от теории")
                    self.results_text.append(f"\nСтрока 1: \"{str1}\"")
                    self.results_text.append(f"Хеш: {get_hash(str1, bits)}")
                    self.results_text.append(f"\nСтрока 2: \"{str2}\"")
                    self.results_text.append(f"Хеш: {get_hash(str2, bits)}")
                    self.results_text.append("Полные SHA-256 хеши (для проверки):")
                    self.results_text.append(f"Строка 1: {compute_full_hash(str1)}")
                    self.results_text.append(f"Строка 2: {compute_full_hash(str2)}")
                case _:
                    self.results_text.append(f"Коллизия не найдена за {attempts} попыток.")
                    self.results_text.append("Попробуйте увеличить максимальное количество попыток.")
        except Exception as e:
            self.on_attack_error(f"Ошибка обработки результатов: {e}")
        finally:
            self.attack_btn.setEnabled(True)

    def on_attack_error(self, error_msg: str) -> None:
        """Обрабатывает ошибки, возникшие в потоке поиска коллизии."""
        QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{error_msg}")
        self.attack_btn.setEnabled(True)

    def start_experiments(self) -> None:
        """Запускает серию экспериментов в фоновом потоке."""
        try:
            bits = int(self.exp_hash_combo.currentText())
            count = self.exp_count_spin.value()
            max_attempts = self.exp_max_attempts_spin.value()

            self.exp_btn.setEnabled(False)
            self.exp_table.setRowCount(0)
            self.exp_progress_bar.setMaximum(count)
            self.exp_progress_bar.setValue(0)

            self.experiments_thread = ExperimentsThread(bits, count, max_attempts)
            self.experiments_thread.progress.connect(self.update_experiment_progress)
            self.experiments_thread.finished.connect(self.on_experiments_finished)
            self.experiments_thread.error.connect(self.on_experiments_error)
            self.experiments_thread.start()
        except Exception as e:
            self.on_experiments_error(str(e))

    def update_experiment_progress(self, current: int, total: int) -> None:
        """Обновляет индикатор прогресса серии экспериментов."""
        self.exp_progress_bar.setValue(current)

    def on_experiments_finished(self, results: list, bits: int) -> None:
        """Обрабатывает результаты серии экспериментов и обновляет таблицу."""
        try:
            self.exp_table.setRowCount(len(results) + 1)
            for row, (num, str1, str2, attempts) in enumerate(results):
                self.exp_table.setItem(row, 0, QTableWidgetItem(str(num)))
                self.exp_table.setItem(row, 1, QTableWidgetItem(str1))
                self.exp_table.setItem(row, 2, QTableWidgetItem(str2))
                self.exp_table.setItem(row, 3, QTableWidgetItem(str(attempts)))

            expected = get_expected_attempts(bits)
            self.exp_table.setItem(len(results), 0, QTableWidgetItem("Теория"))
            self.exp_table.setItem(len(results), 1, QTableWidgetItem("—"))
            self.exp_table.setItem(len(results), 2, QTableWidgetItem("—"))
            self.exp_table.setItem(len(results), 3, QTableWidgetItem(f"~{expected}"))
        except Exception as e:
            self.on_experiments_error(f"Ошибка обновления таблицы: {e}")
        finally:
            self.exp_btn.setEnabled(True)

    def on_experiments_error(self, error_msg: str) -> None:
        """Обрабатывает ошибки, возникшие в потоке экспериментов."""
        QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{error_msg}")
        self.exp_btn.setEnabled(True)

def run_gui() -> None:
    """Запускает приложение с графическим интерфейсом."""
    try:
        app = QApplication(sys.argv)
        window = BirthdayAttackGUI()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Критическая ошибка при запуске GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_gui()