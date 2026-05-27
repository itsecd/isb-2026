import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from crypto_utils import HybridCryptoSystem, HybridCryptoError
from file_utils import FileService


class CryptoApp(QWidget):
    """Главное окно графического интерфейса для управления гибридной криптосистемой."""

    def __init__(self):
        """Инициализирует графические компоненты, стили интерфейса и логику приложения."""
        super().__init__()

        self.settings = None
        self._file_service = FileService()
        self._crypto_system = HybridCryptoSystem()

        self.setWindowTitle("Гибридная криптосистема RSA + AES")
        self.resize(760, 520)

        self.create_widgets()
        self.create_layout()
        self.connect_buttons()
        self.set_styles()

        self.try_load_from_args()
        self.log("Приложение запущено")

    def create_widgets(self) -> None:
        """Создает элементы управления пользовательского интерфейса (кнопки, поля ввода, списки)."""
        self.title_label = QLabel("Гибридная криптосистема RSA + AES")
        self.subtitle_label = QLabel("AES-CBC для файла, RSA-OAEP для ключа AES")

        self.config_path_edit = QLineEdit()
        self.config_path_edit.setPlaceholderText("Укажите путь к settings.json")

        self.choose_config_button = QPushButton("Выбрать")
        self.load_config_button = QPushButton("Загрузить настройки")

        self.input_file_edit = QLineEdit()
        self.encrypted_file_edit = QLineEdit()
        self.decrypted_file_edit = QLineEdit()
        self.encrypted_key_edit = QLineEdit()
        self.public_key_edit = QLineEdit()
        self.private_key_edit = QLineEdit()

        self.path_edits = (
            self.input_file_edit,
            self.encrypted_file_edit,
            self.decrypted_file_edit,
            self.encrypted_key_edit,
            self.public_key_edit,
            self.private_key_edit,
        )

        for edit in self.path_edits:
            edit.setReadOnly(True)

        self.aes_size_box = QComboBox()
        self.aes_size_box.addItems(("128", "192", "256"))

        self.rsa_size_edit = QLineEdit()
        self.rsa_exponent_edit = QLineEdit()
        self.rsa_size_edit.setReadOnly(True)
        self.rsa_exponent_edit.setReadOnly(True)

        self.generate_button = QPushButton("Сгенерировать ключи")
        self.encrypt_button = QPushButton("Зашифровать файл")
        self.decrypt_button = QPushButton("Расшифровать файл")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

    def create_layout(self) -> None:
        """Компонует виджеты в группы и настраивает сеточную геометрию окна."""
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        config_group = QGroupBox("Файл настроек")
        config_layout = QHBoxLayout()
        config_layout.addWidget(self.config_path_edit)
        config_layout.addWidget(self.choose_config_button)
        config_layout.addWidget(self.load_config_button)
        config_group.setLayout(config_layout)

        paths_group = QGroupBox("Пути из settings.json")
        paths_layout = QGridLayout()

        paths_layout.addWidget(QLabel("Исходный файл:"), 0, 0)
        paths_layout.addWidget(self.input_file_edit, 0, 1)

        paths_layout.addWidget(QLabel("Зашифрованный файл:"), 1, 0)
        paths_layout.addWidget(self.encrypted_file_edit, 1, 1)

        paths_layout.addWidget(QLabel("Расшифрованный файл:"), 2, 0)
        paths_layout.addWidget(self.decrypted_file_edit, 2, 1)

        paths_layout.addWidget(QLabel("Зашифрованный AES-ключ:"), 3, 0)
        paths_layout.addWidget(self.encrypted_key_edit, 3, 1)

        paths_layout.addWidget(QLabel("Открытый RSA-ключ:"), 4, 0)
        paths_layout.addWidget(self.public_key_edit, 4, 1)

        paths_layout.addWidget(QLabel("Закрытый RSA-ключ:"), 5, 0)
        paths_layout.addWidget(self.private_key_edit, 5, 1)

        paths_group.setLayout(paths_layout)

        params_group = QGroupBox("Параметры алгоритмов")
        params_layout = QGridLayout()

        params_layout.addWidget(QLabel("Размер AES-ключа:"), 0, 0)
        params_layout.addWidget(self.aes_size_box, 0, 1)
        params_layout.addWidget(QLabel("бит"), 0, 2)

        params_layout.addWidget(QLabel("Размер RSA-ключа:"), 1, 0)
        params_layout.addWidget(self.rsa_size_edit, 1, 1)
        params_layout.addWidget(QLabel("бит"), 1, 2)

        params_layout.addWidget(QLabel("Открытая экспонента RSA:"), 2, 0)
        params_layout.addWidget(self.rsa_exponent_edit, 2, 1)

        params_group.setLayout(params_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.generate_button)
        buttons_layout.addWidget(self.encrypt_button)
        buttons_layout.addWidget(self.decrypt_button)

        log_group = QGroupBox("Журнал работы")
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_box)
        log_group.setLayout(log_layout)

        main_layout.addWidget(config_group)
        main_layout.addWidget(paths_group)
        main_layout.addWidget(params_group)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(log_group)

        self.setLayout(main_layout)

    def connect_buttons(self) -> None:
        """Связывает сигналы нажатия кнопок (clicked) со слотами-обработчиками класса."""
        self.choose_config_button.clicked.connect(self.choose_config)
        self.load_config_button.clicked.connect(self.load_config)
        self.generate_button.clicked.connect(self.generate_keys_action)
        self.encrypt_button.clicked.connect(self.encrypt_file_action)
        self.decrypt_button.clicked.connect(self.decrypt_file_action)

    def set_styles(self) -> None:
        """Применяет темно-фиолетовую кастомную таблицу стилей CSS (QSS) к приложению."""
        self.setStyleSheet(
            """
            QWidget {
                background-color: #17091f;
                color: #f2e9ff;
                font-size: 14px;
            }
            QLabel {
                color: #f2e9ff;
            }
            QGroupBox {
                border: 1px solid #6b2d91;
                border-radius: 8px;
                margin-top: 12px;
                padding: 10px;
                color: #e6d2ff;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #251030;
                border: 1px solid #7c3aad;
                border-radius: 6px;
                padding: 6px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #6b2d91;
                border: 1px solid #9b55d1;
                border-radius: 7px;
                padding: 8px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #7f3ab0;
            }
            QPushButton:pressed {
                background-color: #4d1f6b;
            }
            """
        )
        self.title_label.setStyleSheet("font-size: 23px; font-weight: bold; color: #ffffff;")
        self.subtitle_label.setStyleSheet("color: #c9a8ff;")

    def try_load_from_args(self) -> None:
        """Проверяет аргументы командной строки и пытается автоматически загрузить конфигурацию."""
        match len(sys.argv) > 1:
            case True:
                self.config_path_edit.setText(sys.argv[1])
                self.load_config()
            case False:
                pass

    def choose_config(self) -> None:
        """Открывает диалоговое окно проводника для интерактивного выбора JSON-файла настроек."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл настроек", "", "JSON files (*.json);;All files (*)"
        )
        match path:
            case "":
                return
            case _:
                self.config_path_edit.setText(path)
                self.load_config()

    def load_config(self) -> None:
        """Считывает выбранный конфигурационный файл и заполняет поля путей и параметров в GUI."""
        path = self.config_path_edit.text().strip()
        match path:
            case "":
                self.show_error(ValueError("Не указан путь к файлу настроек"))
                return
            case _:
                try:
                    self.settings = self._file_service.load_settings(path)
                    self.fill_settings_fields()
                    self.log(f"Настройки загружены: {path}")
                except ValueError as exc:
                    self.show_error(exc)

    def fill_settings_fields(self) -> None:
        """Распределяет значения из словаря настроек по соответствующим виджетам интерфейса.

        Raises:
            KeyError: Если в файле настроек JSON отсутствует один из необходимых параметров.
        """
        try:
            self.input_file_edit.setText(self.settings["input_file"])
            self.encrypted_file_edit.setText(self.settings["encrypted_file"])
            self.decrypted_file_edit.setText(self.settings["decrypted_file"])
            self.encrypted_key_edit.setText(self.settings["encrypted_key_file"])
            self.public_key_edit.setText(self.settings["public_key_file"])
            self.private_key_edit.setText(self.settings["private_key_file"])

            self.aes_size_box.setCurrentText(str(self.settings["aes_key_size"]))
            self.rsa_size_edit.setText(str(self.settings["rsa_key_size"]))
            self.rsa_exponent_edit.setText(str(self.settings["rsa_public_exponent"]))
        except KeyError as exc:
            raise KeyError(f"В settings.json отсутствует параметр: {exc}") from exc

    def get_checked_settings(self) -> dict:
        """Проверяет, загружены ли настройки, и обновляет размер сессионного ключа AES из комбобокса.

        Returns:
            dict: Актуальный словарь настроек.

        Raises:
            RuntimeError: Если пользователь пытается выполнить действие без загрузки файла конфигурации.
        """
        match self.settings is None:
            case True:
                raise RuntimeError("Сначала загрузите файл настроек")
            case False:
                self.settings["aes_key_size"] = int(self.aes_size_box.currentText())
                return self.settings

    def generate_keys_action(self) -> None:
        """Слот кнопки генерации ключей. Запускает процесс Сценария 1 и логирует этапы."""
        try:
            settings = self.get_checked_settings()

            self.log("Генерация ключей начата")
            self.log("Создается AES-ключ")
            self.log("Создается пара RSA-ключей")

            self._crypto_system.run_key_generation(
                settings["encrypted_key_file"],
                settings["public_key_file"],
                settings["private_key_file"],
                settings["aes_key_size"],
                settings["rsa_key_size"],
                settings["rsa_public_exponent"],
            )

            self.log("AES-ключ зашифрован открытым RSA-ключом")
            self.log("Ключи успешно сохранены")
            self.show_info("Ключи успешно созданы")
        except (RuntimeError, KeyError, HybridCryptoError) as exc:
            self.show_error(exc)

    def encrypt_file_action(self) -> None:
        """Слот кнопки шифрования файла. Реализует Сценарий 2 с детальным логированием хода операции."""
        try:
            settings = self.get_checked_settings()

            self.log("Шифрование файла начато")
            self.log("AES-ключ расшифровывается закрытым RSA-ключом")

            self._crypto_system.run_encryption(
                settings["input_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["encrypted_file"],
            )

            self.log(f"Файл зашифрован: {settings['encrypted_file']}")
            self.show_info("Файл успешно зашифрован")
        except (RuntimeError, KeyError, HybridCryptoError, ValueError) as exc:
            self.show_error(exc)

    def decrypt_file_action(self) -> None:
        """Слот кнопки дешифрования. Выполняет Сценарий 3 и сообщает пользователю о результате."""
        try:
            settings = self.get_checked_settings()

            self.log("Дешифрование файла начато")
            self.log("AES-ключ расшифровывается закрытым RSA-ключом")

            self._crypto_system.run_decryption(
                settings["encrypted_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["decrypted_file"],
            )

            self.log(f"Файл расшифрован: {settings['decrypted_file']}")
            self.show_info("Файл успешно расшифрован")
        except (RuntimeError, KeyError, HybridCryptoError, ValueError) as exc:
            self.show_error(exc)

    def log(self, text: str) -> None:
        """Добавляет строку с системным сообщением в текстовое поле Журнала работы на экране.

        Args:
            text (str): Текст сообщения.
        """
        self.log_box.append(text)

    def show_error(self, error: Exception) -> None:
        """Отображает возникшую ошибку в окне QMessageBox и дублирует её в лог.

        Args:
            error (Exception): Объект исключения.
        """
        self.log(f"Ошибка: {error}")
        QMessageBox.critical(self, "Ошибка", str(error))

    def show_info(self, text: str) -> None:
        """Выводит информационное модальное уведомление об успешном завершении операции.

        Args:
            text (str): Текст сообщения.
        """
        QMessageBox.information(self, "Готово", text)


def main():
    """Точка входа: инициализирует и запускает QT-приложение."""
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()