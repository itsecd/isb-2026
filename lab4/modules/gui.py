import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTextEdit, QSpinBox,
    QMessageBox, QProgressBar, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from modules.auth import register_user, authenticate_user
from modules.hashing import (
    demonstrate_avalanche_effect,
    find_collision_simple
)


class CollisionSignals(QObject):
    """
    Сигналы для обновления GUI из потока поиска коллизии.
    """
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)


class AuthWindow(QMainWindow):
    """
    Главное окно приложения аутентификации.

    Содержит вкладки для регистрации, входа, демонстрации
    лавинного эффекта и поиска коллизии.
    """

    def __init__(self, users_file: str = "data/users.json",
                 algorithm: str = "sha256"):
        """
        Инициализирует главное окно.

        Args:
            users_file (str): путь к файлу базы пользователей.
            algorithm (str): алгоритм хеширования по умолчанию.
        """
        super().__init__()
        self.users_file = users_file
        self.algorithm = algorithm
        self.collision_signals = CollisionSignals()
        self.collision_signals.finished.connect(self.on_collision_finished)

        self.setWindowTitle("Лабораторная работа №4 — Хеш-функции")
        self.setMinimumSize(600, 500)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Настраивает пользовательский интерфейс.
        Создаёт вкладки и наполняет их элементами.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        tabs.addTab(self._create_register_tab(), "Регистрация")
        tabs.addTab(self._create_login_tab(), "Вход")
        tabs.addTab(self._create_avalanche_tab(), "Лавинный эффект")
        tabs.addTab(self._create_collision_tab(), "Поиск коллизии")

    def _create_register_tab(self) -> QWidget:
        """
        Создаёт вкладку регистрации нового пользователя.

        Returns:
            QWidget: виджет вкладки.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Регистрация нового пользователя")
        form_layout = QFormLayout()
        group.setLayout(form_layout)

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Введите логин")
        form_layout.addRow("Логин:", self.reg_username)

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Введите пароль")
        self.reg_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.reg_password)

        self.reg_algorithm = QComboBox()
        self.reg_algorithm.addItems(["sha256", "bcrypt"])
        form_layout.addRow("Алгоритм:", self.reg_algorithm)

        layout.addWidget(group)

        self.reg_button = QPushButton("Зарегистрироваться")
        self.reg_button.clicked.connect(self._on_register)
        layout.addWidget(self.reg_button)

        self.reg_output = QTextEdit()
        self.reg_output.setReadOnly(True)
        self.reg_output.setMaximumHeight(150)
        layout.addWidget(self.reg_output)

        layout.addStretch()
        return tab

    def _create_login_tab(self) -> QWidget:
        """
        Создаёт вкладку входа в систему.

        Returns:
            QWidget: виджет вкладки.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Вход в систему")
        form_layout = QFormLayout()
        group.setLayout(form_layout)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Введите логин")
        form_layout.addRow("Логин:", self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Введите пароль")
        self.login_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Пароль:", self.login_password)

        layout.addWidget(group)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self._on_login)
        layout.addWidget(self.login_button)

        self.login_output = QTextEdit()
        self.login_output.setReadOnly(True)
        self.login_output.setMaximumHeight(100)
        layout.addWidget(self.login_output)

        layout.addStretch()
        return tab

    def _create_avalanche_tab(self) -> QWidget:
        """
        Создаёт вкладку демонстрации лавинного эффекта.

        Returns:
            QWidget: виджет вкладки.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Демонстрация лавинного эффекта SHA-256")
        form_layout = QFormLayout()
        group.setLayout(form_layout)

        self.av_msg1 = QLineEdit()
        self.av_msg1.setText("password123")
        form_layout.addRow("Сообщение 1:", self.av_msg1)

        self.av_msg2 = QLineEdit()
        self.av_msg2.setText("password124")
        form_layout.addRow("Сообщение 2:", self.av_msg2)

        layout.addWidget(group)

        self.av_button = QPushButton("Показать лавинный эффект")
        self.av_button.clicked.connect(self._on_avalanche)
        layout.addWidget(self.av_button)

        self.av_output = QTextEdit()
        self.av_output.setReadOnly(True)
        layout.addWidget(self.av_output)

        layout.addStretch()
        return tab

    def _create_collision_tab(self) -> QWidget:
        """
        Создаёт вкладку поиска коллизии с прогресс-баром.

        Returns:
            QWidget: виджет вкладки.
        """
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        group = QGroupBox("Поиск коллизии (усечённый SHA-256)")
        form_layout = QFormLayout()
        group.setLayout(form_layout)

        self.col_bytes = QSpinBox()
        self.col_bytes.setRange(1, 4)
        self.col_bytes.setValue(2)
        self.col_bytes.setToolTip("Количество байт хеша для сравнения (1-4)")
        form_layout.addRow("Байт для сравнения:", self.col_bytes)

        layout.addWidget(group)

        button_layout = QHBoxLayout()

        self.col_button = QPushButton("Начать поиск")
        self.col_button.clicked.connect(self._on_collision_search)
        button_layout.addWidget(self.col_button)

        self.col_stop_button = QPushButton("Остановить")
        self.col_stop_button.clicked.connect(self._on_collision_stop)
        self.col_stop_button.setEnabled(False)
        button_layout.addWidget(self.col_stop_button)

        layout.addLayout(button_layout)

        self.col_progress = QProgressBar()
        self.col_progress.setRange(0, 0)
        self.col_progress.setVisible(False)
        layout.addWidget(self.col_progress)

        self.col_output = QTextEdit()
        self.col_output.setReadOnly(True)
        layout.addWidget(self.col_output)

        layout.addStretch()

        self._collision_thread = None
        self._collision_running = False

        return tab

    def _on_register(self) -> None:
        """
        Обработчик кнопки регистрации.
        """
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        algorithm = self.reg_algorithm.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка",
                               "Логин и пароль не могут быть пустыми.")
            return

        try:
            result = register_user(username, password,
                                  self.users_file, algorithm)
            if result["success"]:
                self.reg_output.setText(
                    f"Успех: {result['message']}\n"
                    f"Алгоритм: {result['user_data']['algorithm']}\n"
                    f"Хеш: {result['user_data']['hash'][:50]}..."
                )
                self.reg_username.clear()
                self.reg_password.clear()
            else:
                self.reg_output.setText(f"Ошибка: {result['message']}")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка",
                                f"Произошла ошибка: {e}")

    def _on_login(self) -> None:
        """
        Обработчик кнопки входа.
        """
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка",
                               "Логин и пароль не могут быть пустыми.")
            return

        try:
            result = authenticate_user(username, password, self.users_file)
            if result["success"]:
                self.login_output.setText(
                    f"Успех: {result['message']}\n"
                    f"Алгоритм: {result['user_data']['algorithm']}\n"
                    f"Создан: {result['user_data']['created_at']}"
                )
            else:
                self.login_output.setText(f"Ошибка: {result['message']}")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка",
                                f"Произошла ошибка: {e}")

    def _on_avalanche(self) -> None:
        """
        Обработчик кнопки демонстрации лавинного эффекта.
        """
        import hashlib

        msg1 = self.av_msg1.text()
        msg2 = self.av_msg2.text()

        hash1 = hashlib.sha256(msg1.encode('utf-8')).hexdigest()
        hash2 = hashlib.sha256(msg2.encode('utf-8')).hexdigest()

        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        diff_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
        diff_percent = (diff_bits / 256) * 100

        output = (
            f"Сообщение 1: {msg1}\n"
            f"Хеш 1: {hash1}\n\n"
            f"Сообщение 2: {msg2}\n"
            f"Хеш 2: {hash2}\n\n"
            f"Изменено бит: {diff_bits} из 256 ({diff_percent:.1f}%)\n"
            f"Ожидаемое значение при лавинном эффекте: около 50%"
        )
        self.av_output.setText(output)

    def _on_collision_search(self) -> None:
        """
        Обработчик кнопки поиска коллизии.
        Запускает поиск в отдельном потоке.
        """
        self.col_output.clear()
        num_bytes = self.col_bytes.value()

        self.col_button.setEnabled(False)
        self.col_stop_button.setEnabled(True)
        self.col_progress.setVisible(True)
        self.col_output.setText(f"Идёт поиск коллизии для {num_bytes} байт "
                               f"({num_bytes * 2} шестнадцатеричных символов)...\n"
                               f"Это может занять некоторое время.")

        self._collision_running = True
        self._collision_thread = threading.Thread(
            target=self._collision_worker,
            args=(num_bytes,),
            daemon=True
        )
        self._collision_thread.start()

    def _collision_worker(self, num_bytes: int) -> None:
        """
        Рабочий метод для поиска коллизии в отдельном потоке.

        Args:
            num_bytes (int): количество байт для сравнения.
        """
        result = find_collision_simple(num_bytes, show_progress=False)
        if self._collision_running:
            self.collision_signals.finished.emit(result)

    def on_collision_finished(self, result: dict) -> None:
        """
        Обработчик завершения поиска коллизии.

        Args:
            result (dict): результат поиска из find_collision_simple.
        """
        self.col_button.setEnabled(True)
        self.col_stop_button.setEnabled(False)
        self.col_progress.setVisible(False)
        self._collision_running = False

        if result["message1"] is not None:
            output = (
                f"Коллизия найдена!\n\n"
                f"Сообщение 1: {result['message1']}\n"
                f"Сообщение 2: {result['message2']}\n"
                f"Общий префикс хеша: {result['hash_prefix']}\n"
                f"Количество попыток: {result['attempts']}\n"
                f"Затраченное время: {result['time_seconds']:.2f} сек"
            )
        else:
            output = (
                f"Коллизия не найдена.\n"
                f"Количество попыток: {result['attempts']}\n"
                f"Затраченное время: {result['time_seconds']:.2f} сек"
            )

        self.col_output.setText(output)

    def _on_collision_stop(self) -> None:
        """
        Обработчик кнопки остановки поиска коллизии.
        """
        self._collision_running = False
        self.col_button.setEnabled(True)
        self.col_stop_button.setEnabled(False)
        self.col_progress.setVisible(False)
        self.col_output.append("\nПоиск остановлен пользователем.")


def run_gui(users_file: str = "data/users.json",
            algorithm: str = "sha256") -> None:
    """
    Запускает графический интерфейс приложения.

    Args:
        users_file (str): путь к файлу базы пользователей.
        algorithm (str): алгоритм хеширования по умолчанию.
    """
    app = QApplication(sys.argv)
    window = AuthWindow(users_file, algorithm)
    window.show()
    sys.exit(app.exec_())