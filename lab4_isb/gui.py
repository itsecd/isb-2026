import sys

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSpinBox,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QProgressBar,
)

from main import run_collision_experiments


class ExperimentWorker(QObject):
    """
    Рабочий объект для запуска экспериментов в отдельном потоке.
    """

    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(
        self,
        length: int,
        bits_list: list[int],
        num_experiments: int,
        file_name: str,
        stats_file: str
    ):
        """
        Инициализация рабочего объекта.
        :param length: длина случайных строк
        :param bits_list: список длин укороченного хеша
        :param num_experiments: количество экспериментов
        :param file_name: путь к CSV-файлу с коллизиями
        :param stats_file: путь к CSV-файлу со статистикой
        :return: не возвращается
        """

        super().__init__()
        self.length = length
        self.bits_list = bits_list
        self.num_experiments = num_experiments
        self.file_name = file_name
        self.stats_file = stats_file

    def run(self) -> None:
        """
        Запуск экспериментов.
        :return: не возвращается
        """

        try:
            stats = run_collision_experiments(
                length=self.length,
                bits_list=self.bits_list,
                num_experiments=self.num_experiments,
                file_name=self.file_name,
                stats_file=self.stats_file
            )
            self.finished.emit(stats)
        except Exception as e:
            self.error.emit(str(e))


class CollisionApp(QWidget):
    """
    Графический интерфейс для запуска экспериментов поиска коллизий.
    """

    def __init__(self):
        """
        Инициализация главного окна.
        :return: не возвращается
        """

        super().__init__()
        self.thread = None
        self.worker = None
        self.setWindowTitle("Hash Collision Experiments")
        self.setMinimumSize(760, 560)
        self.length_input = QSpinBox()
        self.length_input.setMinimum(1)
        self.length_input.setMaximum(1000)
        self.length_input.setValue(10)
        self.experiments_input = QSpinBox()
        self.experiments_input.setMinimum(1)
        self.experiments_input.setMaximum(1_000_000)
        self.experiments_input.setValue(1000)
        self.bits_input = QComboBox()
        self.bits_input.addItems(["all", "8", "12", "16"])
        self.collision_file_input = QLineEdit("collisions.csv")
        self.stats_file_input = QLineEdit("stats.csv")
        self.collision_file_button = QPushButton("Browse")
        self.stats_file_button = QPushButton("Browse")
        self.run_button = QPushButton("Run experiments")
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.setup_ui()
        self.setup_style()
        self.connect_signals()

    def setup_ui(self) -> None:
        """
        Создание элементов интерфейса.
        :return: не возвращается
        """

        main_layout = QVBoxLayout()
        title = QLabel("Shortened SHA-256 Collision Search")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Run experiments for 8, 12, or 16-bit shortened hashes and save statistics to CSV.")
        subtitle.setObjectName("subtitleLabel")
        settings_group = QGroupBox("Experiment settings")
        settings_layout = QFormLayout()
        settings_layout.addRow("Random string length:", self.length_input)
        settings_layout.addRow("Experiments:", self.experiments_input)
        settings_layout.addRow("Hash length:", self.bits_input)
        settings_group.setLayout(settings_layout)
        files_group = QGroupBox("Output files")
        files_layout = QVBoxLayout()
        collision_layout = QHBoxLayout()
        collision_layout.addWidget(QLabel("Collisions CSV:"))
        collision_layout.addWidget(self.collision_file_input)
        collision_layout.addWidget(self.collision_file_button)
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel("Statistics CSV:"))
        stats_layout.addWidget(self.stats_file_input)
        stats_layout.addWidget(self.stats_file_button)
        files_layout.addLayout(collision_layout)
        files_layout.addLayout(stats_layout)
        files_group.setLayout(files_layout)
        run_layout = QHBoxLayout()
        run_layout.addWidget(self.run_button)
        run_layout.addWidget(self.status_label)
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output)
        output_group.setLayout(output_layout)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(settings_group)
        main_layout.addWidget(files_group)
        main_layout.addLayout(run_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(output_group)
        self.setLayout(main_layout)

    def setup_style(self) -> None:
        """
        Настройка внешнего вида интерфейса.
        :return: не возвращается
        """

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fb;
                color: #1f2937;
                font-size: 14px;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #d8dee9;
                border-radius: 10px;
                margin-top: 12px;
                padding: 12px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #111827;
            }
            QLabel#subtitleLabel {
                color: #6b7280;
                margin-bottom: 6px;
            }
            QLineEdit, QSpinBox, QComboBox, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 7px;
            }
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 13px;
            }
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 9px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
            QProgressBar {
                background-color: #e5e7eb;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                height: 18px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 8px;
            }
        """)

    def connect_signals(self) -> None:
        """
        Подключение сигналов кнопок к обработчикам.
        :return: не возвращается
        """

        self.collision_file_button.clicked.connect(self.choose_collision_file)
        self.stats_file_button.clicked.connect(self.choose_stats_file)
        self.run_button.clicked.connect(self.start_experiments)

    def choose_collision_file(self) -> None:
        """
        Выбор файла для сохранения найденных коллизий.
        :return: не возвращается
        """

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Choose collisions CSV file",
            "collisions.csv",
            "CSV files (*.csv);;All files (*)"
        )
        if filename:
            self.collision_file_input.setText(filename)

    def choose_stats_file(self) -> None:
        """
        Выбор файла для сохранения статистики.
        :return: не возвращается
        """

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Choose statistics CSV file",
            "stats.csv",
            "CSV files (*.csv);;All files (*)"
        )
        if filename:
            self.stats_file_input.setText(filename)

    def get_bits_list(self) -> list[int]:
        """
        Получение выбранной длины укороченного хеша.
        :return: список длин хеша в битах
        """

        value = self.bits_input.currentText()
        if value == "all":
            return [8, 12, 16]
        return [int(value)]

    def start_experiments(self) -> None:
        """
        Запуск экспериментов из интерфейса.
        :return: не возвращается
        """

        length = self.length_input.value()
        num_experiments = self.experiments_input.value()
        bits_list = self.get_bits_list()
        collision_file = self.collision_file_input.text().strip()
        stats_file = self.stats_file_input.text().strip()
        if not collision_file:
            QMessageBox.warning(self, "Error", "Collision CSV file path is empty")
            return
        if not stats_file:
            QMessageBox.warning(self, "Error", "Statistics CSV file path is empty")
            return
        self.output.clear()
        self.output.append("Experiments started")
        self.output.append(f"Random string length: {length}")
        self.output.append(f"Hash lengths: {bits_list}")
        self.output.append(f"Experiments per hash length: {num_experiments}")
        self.output.append(f"Collision file: {collision_file}")
        self.output.append(f"Statistics file: {stats_file}")
        self.status_label.setText("Running...")
        self.run_button.setEnabled(False)
        self.progress_bar.setRange(0, 0)
        self.thread = QThread()
        self.worker = ExperimentWorker(length, bits_list, num_experiments, collision_file, stats_file)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_experiments_finished)
        self.worker.error.connect(self.on_experiments_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_experiments_finished(self, stats: list[dict]) -> None:
        """
        Обработка успешного завершения экспериментов.
        :param stats: список словарей со статистикой
        :return: не возвращается
        """

        self.run_button.setEnabled(True)
        self.status_label.setText("Completed")
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.output.append("")
        self.output.append("Experiments completed successfully")
        self.output.append("")
        self.output.append("Statistics:")
        for row in stats:
            self.output.append(
                f"Bits: {row['bits']} | "
                f"Experiments: {row['experiments']} | "
                f"Average: {row['average_attempts']} | "
                f"Min: {row['min_attempts']} | "
                f"Max: {row['max_attempts']} | "
                f"Theory: {row['theory_attempts']}"
            )

    def on_experiments_error(self, message: str) -> None:
        """
        Обработка ошибки во время экспериментов.
        :param message: текст ошибки
        :return: не возвращается
        """

        self.run_button.setEnabled(True)
        self.status_label.setText("Error")
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.output.append("")
        self.output.append("Error:")
        self.output.append(message)
        QMessageBox.critical(self, "Error", message)


def main() -> None:
    """
    Запуск PyQt-приложения.
    :return: не возвращается
    """

    app = QApplication(sys.argv)
    window = CollisionApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()