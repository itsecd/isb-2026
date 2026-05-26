import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QTextEdit,
)
from hasher import calculate_file_hash, save_hash_to_file, verify_file_integrity


class IntegrityCheckerApp(QMainWindow):
    """
    Класс главного окна графического интерфейса приложения.

    Обеспечивает визуальный выбор файлов, запуск процессов вычисления контрольных сумм
    и проверку целостности с логированием результатов в текстовое поле.
    """

    def __init__(self) -> None:
        """Инициализирует графический интерфейс и устанавливает геометрию окна."""
        super().__init__()
        self.setWindowTitle("Контроль целостности файлов (SHA-256)")
        self.setGeometry(200, 200, 600, 350)
        self.init_ui()

    def init_ui(self) -> None:
        """Постраивает сетку элементов интерфейса (Layouts) и привязывает обработчики событий."""
        main_widget = QWidget()
        layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        self.file_label = QLabel("Файл:")
        self.file_input = QLineEdit()
        self.file_btn = QPushButton("Обзор...")
        self.file_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_btn)
        layout.addLayout(file_layout)

        hash_layout = QHBoxLayout()
        self.hash_label = QLabel("Файл хеша:")
        self.hash_input = QLineEdit()
        self.hash_btn = QPushButton("Обзор...")
        self.hash_btn.clicked.connect(self.browse_hash_file)
        hash_layout.addWidget(self.hash_label)
        hash_layout.addWidget(self.hash_input)
        hash_layout.addWidget(self.hash_btn)
        layout.addLayout(hash_layout)

        btn_layout = QHBoxLayout()
        self.calc_btn = QPushButton("Рассчитать и сохранить хеш")
        self.calc_btn.clicked.connect(self.action_calc_and_save)
        self.verify_btn = QPushButton("Проверить целостность")
        self.verify_btn.clicked.connect(self.action_verify)
        btn_layout.addWidget(self.calc_btn)
        btn_layout.addWidget(self.verify_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("Лог выполнения:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def browse_file(self) -> None:
        """Вызывает диалоговое окно для выбора любого исследуемого файла."""
        f_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл для хеширования")
        if f_path:
            self.file_input.setText(f_path)

    def browse_hash_file(self) -> None:
        """Вызывает диалоговое окно для выбора или создания .sha256 файла сигнатуры."""
        f_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл сигнатуры хеша", "", "Hash Files (*.sha256 *.txt)"
        )
        if f_path:
            self.hash_input.setText(f_path)

    def action_calc_and_save(self) -> None:
        """
        Слот-обработчик для расчета и сохранения контрольной суммы.

        Raises:
            OSError: В случае сбоя файловой системы, обрабатывается внутри метода.
        """
        f_path = self.file_input.text()
        h_path = self.hash_input.text()

        if not f_path:
            QMessageBox.critical(
                self, "Ошибка", "Укажите путь к целевому файлу!")
            return
        if not h_path:
            h_path = f_path + ".sha256"
            self.hash_input.setText(h_path)

        try:
            h_val = calculate_file_hash(f_path)
            save_hash_to_file(h_val, h_path)
            self.log_output.append(
                f"[ОК] Хеш рассчитан и успешно сохранен в: {h_path}")
            self.log_output.append(f"SHA-256: {h_val}\n")
        except OSError as e:
            QMessageBox.critical(
                self, "Ошибка файловой системы", f"Сбой ввода-вывода: {e}")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            QMessageBox.critical(self, "Критическая ошибка",
                                 f"Непредвиденное исключение: {err}")
            raise

    def action_verify(self) -> None:
        """
        Слот-обработчик для запуска процесса верификации целостности данных.

        Raises:
            OSError: В случае отсутствия файлов, обрабатывается внутри метода.
        """
        f_path = self.file_input.text()
        h_path = self.hash_input.text()

        if not f_path or not h_path:
            QMessageBox.critical(
                self, "Ошибка", "Необходимо заполнить оба пути (файл и хеш)!")
            return

        try:
            is_valid, cur_hash, exp_hash = verify_file_integrity(
                f_path, h_path)
            self.log_output.append(f"--- Проверка сигнатуры для: {f_path} ---")
            self.log_output.append(f"Ожидаемый (из файла): {exp_hash}")
            self.log_output.append(f"Текущий (вычисленный): {cur_hash}")

            if is_valid:
                self.log_output.append(
                    "Результат: ЦЕЛОСТНОСТЬ ХЕША ПОДТВЕРЖДЕНА\n")
                QMessageBox.information(
                    self, "Успех", "Модификаций не обнаружено. Файл целостен.")
            else:
                self.log_output.append(
                    "Результат: ВНИМАНИЕ! ОБНАРУЖЕНА ИЗМЕНЕНИЕ ДАННЫХ\n")
                QMessageBox.warning(
                    self, "Внимание", "Критическое несовпадение контрольных сумм!")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Файл не найден", str(e))
        except OSError as e:
            QMessageBox.critical(
                self, "Ошибка ввода-вывода", f"Сбой доступа: {e}")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            QMessageBox.critical(self, "Критическая ошибка",
                                 f"Непредвиденное исключение: {err}")
            raise


def run_gui() -> None:
    """
    Инициализирует контекст Qt приложения и запускает бесконечный цикл обработки событий GUI.

    Raises:
        Exception: Любые критические исключения среды Qt, логируются и пробрасываются выше.
    """
    try:
        app = QApplication(sys.argv)
        window = IntegrityCheckerApp()
        window.show()
        sys.exit(app.exec())
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
