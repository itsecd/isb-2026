import os
import hashlib
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QTextEdit,
    QGroupBox,
    QMessageBox,
    QSpinBox,
    QProgressBar,
)
from hash import calculating_hash, integrity_check, collision_demo
from load_and_save_hash import save_hash, load_hash


class Hash_app(QMainWindow):
    def __init__(self) -> None:
        """
        Инициализирует приложение и его базовые атрибуты.
        """
        super().__init__()
        self.file_path = None
        self.hash_file_path = None
        self.initUI()

    def initUI(self) -> None:
        """
        Создает элементы графического интерфейса и настраивает их расположение.
        """
        self.setWindowTitle("Проверка целостности файлов")
        self.resize(600, 720)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        group_files = QGroupBox("Выбор файлов")
        layout_files = QVBoxLayout()

        layout_src = QHBoxLayout()
        self.lbl_file = QLabel("Исходный файл: Не выбран")
        btn_select_file = QPushButton("Выбрать файл")
        btn_select_file.clicked.connect(self.select_file)
        layout_src.addWidget(self.lbl_file)
        layout_src.addWidget(btn_select_file)

        layout_hash = QHBoxLayout()
        self.lbl_hash_file = QLabel("Файл хеша: Не выбран")
        btn_select_hash_file = QPushButton("Выбрать файл хеша")
        btn_select_hash_file.clicked.connect(self.select_hash_file)
        layout_hash.addWidget(self.lbl_hash_file)
        layout_hash.addWidget(btn_select_hash_file)

        layout_files.addLayout(layout_src)
        layout_files.addLayout(layout_hash)
        group_files.setLayout(layout_files)

        group_actions = QGroupBox("Действия")
        layout_actions = QHBoxLayout()

        btn_generate = QPushButton("Рассчитать и сохранить хеш")
        btn_generate.clicked.connect(self.generate_and_save_hash)
        btn_generate.setMinimumHeight(40)

        btn_verify = QPushButton("Проверить целостность")
        btn_verify.clicked.connect(self.verify_file)
        btn_verify.setMinimumHeight(40)

        layout_actions.addWidget(btn_generate)
        layout_actions.addWidget(btn_verify)
        group_actions.setLayout(layout_actions)

        group_collision = QGroupBox("Демонстрация коллизий (усеченных)")
        layout_collision = QVBoxLayout()

        layout_inputs = QHBoxLayout()
        lbl_prefix = QLabel("Сложность (длина совпадения префикса):")
        self.spin_prefix = QSpinBox()

        self.spin_prefix.setRange(1, 20)
        self.spin_prefix.setValue(4)

        btn_run_collision = QPushButton("Найти совпадение хешей")
        btn_run_collision.clicked.connect(self.run_collision)
        btn_run_collision.setMinimumHeight(35)

        layout_inputs.addWidget(lbl_prefix)
        layout_inputs.addWidget(self.spin_prefix)
        layout_inputs.addWidget(btn_run_collision)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        layout_collision.addLayout(layout_inputs)
        layout_collision.addWidget(self.progress_bar)
        group_collision.setLayout(layout_collision)

        group_log = QGroupBox("Результат (Журнал)")
        layout_log = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout_log.addWidget(self.log_text)
        group_log.setLayout(layout_log)

        main_layout.addWidget(group_files)
        main_layout.addWidget(group_actions)
        main_layout.addWidget(group_collision)
        main_layout.addWidget(group_log)

    def print_log(self, message: str) -> None:
        """
        Добавляет текстовое сообщение в окно журнала событий.
        """
        self.log_text.append(message)

    def select_file(self) -> None:
        """
        Вызывает диалоговое окно для выбора исходного проверяемого файла.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Выберите исходный файл")
        if path:
            self.file_path = path
            self.lbl_file.setText(f"Исходный файл: {os.path.basename(path)}")
            self.print_log(f"Выбран файл: {path}")

    def generate_and_save_hash(self) -> None:
        """
        Вычисляет контрольную сумму файла и сохраняет результат на диск.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите исходный файл!")
            return
        try:
            self.print_log("\nРасчет хеша...")
            hash_value = calculating_hash(self.file_path)
            self.print_log(f" Хеш рассчитан: {hash_value}")

            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить хеш")
            if save_path:
                save_hash(self.file_path, hash_value, save_path)
                self.print_log(f" Хеш успешно сохранен в: {save_path}")
                self.hash_file_path = save_path
                self.lbl_hash_file.setText(f"Файл хеша: {os.path.basename(save_path)}")
        except Exception as e:
            self.print_log(f"Ошибка при создании хеша: {e}")

    def verify_file(self) -> None:
        """
        Сравнивает текущий хеш файла с эталонным и выводит результат проверки.
        """
        if not self.file_path or not self.hash_file_path:
            QMessageBox.warning(
                self, "Ошибка", "Для проверки нужно выбрать исходный файл и файл хеша!"
            )
            return
        try:
            self.print_log("\n Запуск проверки целостности...")
            is_valid = integrity_check(self.file_path, self.hash_file_path)

            self.print_log("=========================================")
            if is_valid:
                self.print_log("Целостность подтверждена. Файл не изменен.")
            else:
                expected_hash = load_hash(self.hash_file_path)
                actual_hash = calculating_hash(self.file_path)
                self.print_log("ЦЕЛОСТНОСТЬ НАРУШЕНА! Файл был изменён.")
                self.print_log(f"   Ожидается: {expected_hash}")
                self.print_log(f"   Получено:  {actual_hash}")
                self.print_log("=========================================")
        except Exception as e:
            self.print_log(f"Ошибка при проверке: {e}")

    def select_hash_file(self) -> None:
        """
        Вызывает диалоговое окно для выбора файла с эталонным хешем.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с хешем")
        if path:
            self.hash_file_path = path
            self.lbl_hash_file.setText(f"Файл хеша: {os.path.basename(path)}")
            self.print_log(f"Выбран файл хеша: {path}")

    def run_collision(self) -> None:
        """
        Инициирует процесс поиска усеченной коллизии.
        """
        prefix_len = self.spin_prefix.value()

        attempts_max = 3000000

        self.progress_bar.setMaximum(attempts_max)
        self.progress_bar.setValue(0)

        self.print_log(f"\nЗапущен поиск совпадения для первых {prefix_len} символов")
        QCoreApplication.processEvents()

        def update_progress(current_step):
            self.progress_bar.setValue(current_step)
            QCoreApplication.processEvents()

        result = collision_demo(
            attempts=attempts_max,
            prefix_len=prefix_len,
            progress_callback=update_progress,
        )

        if result["first"] is not None:
            self.progress_bar.setValue(attempts_max)
        else:
            self.progress_bar.setValue(result["attempts"])

        if result["first"] is not None:
            text1 = result["first"]
            text2 = result["second"]

            hash1 = hashlib.sha256(text1.encode()).hexdigest()
            hash2 = hashlib.sha256(text2.encode()).hexdigest()

            self.print_log("ЧАСТИЧНАЯ КОЛЛИЗИЯ УСПЕШНО НАЙДЕНА!")
            self.print_log(f" Сделано попыток подбора: {result['attempts']}")
            self.print_log(f" Совпавший префикс хеша: {hash1[:prefix_len]}")
            self.print_log("-----------------------------------------")
            self.print_log(f" Текст 1: {text1}")
            self.print_log(f" Полный Хеш 1: {hash1}")
            self.print_log("-----------------------------------------")
            self.print_log(f" Текст 2: {text2}")
            self.print_log(f" Полный Хеш 2: {hash2}")
        else:
            self.print_log(f" Коллизия НЕ НАЙДЕНА за {result['attempts']} попыток.")
