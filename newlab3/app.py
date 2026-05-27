import sys
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)

from exceptions import HybridCryptoError
from file_utils import FileService
from hybrid import HybridCryptoSystem

class CryptoApp(QWidget):
    """Главное окно приложения с использованием вкладок (QTabWidget)."""

    def __init__(self):
        super().__init__()

        self.settings = None
        self._file_service = FileService()
        self._crypto_system = HybridCryptoSystem()

        self.setWindowTitle("Гибридная криптосистема RSA + AES")
        self.resize(800, 550)

        self.create_widgets()
        self.create_layout()
        self.connect_buttons()
        self.set_styles()

        self.try_load_from_args()
        self.log("Приложение успешно запущено. Перейдите во вкладку 'Настройки' для загрузки конфигурации.")

    def create_widgets(self) -> None:
        self.title_label = QLabel("Гибридная криптосистема")
        
        self.tabs = QTabWidget()
        self.tab_settings = QWidget()
        self.tab_operations = QWidget()
        self.tabs.addTab(self.tab_settings, "⚙️ Настройки и пути")
        self.tabs.addTab(self.tab_operations, "🔐 Криптография и Журнал")

        self.config_path_edit = QLineEdit()
        self.config_path_edit.setPlaceholderText("Путь к файлу settings.json...")
        self.choose_config_button = QPushButton("Обзор")
        self.load_config_button = QPushButton("Загрузить")

        self.input_file_edit = QLineEdit()
        self.encrypted_file_edit = QLineEdit()
        self.decrypted_file_edit = QLineEdit()
        self.encrypted_key_edit = QLineEdit()
        self.public_key_edit = QLineEdit()
        self.private_key_edit = QLineEdit()

        for edit in (self.input_file_edit, self.encrypted_file_edit, self.decrypted_file_edit, 
                     self.encrypted_key_edit, self.public_key_edit, self.private_key_edit):
            edit.setReadOnly(True)

        self.aes_size_box = QComboBox()
        self.aes_size_box.addItems(("128", "192", "256"))
        self.rsa_size_edit = QLineEdit()
        self.rsa_size_edit.setReadOnly(True)
        self.rsa_exponent_edit = QLineEdit()
        self.rsa_exponent_edit.setReadOnly(True)

        self.generate_button = QPushButton("1. Сгенерировать ключи")
        self.encrypt_button = QPushButton("2. Зашифровать файл")
        self.decrypt_button = QPushButton("3. Расшифровать файл")
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

    def create_layout(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        settings_layout = QVBoxLayout()
        
        config_group = QGroupBox("Управление конфигурацией (JSON)")
        config_layout = QHBoxLayout()
        config_layout.addWidget(self.config_path_edit)
        config_layout.addWidget(self.choose_config_button)
        config_layout.addWidget(self.load_config_button)
        config_group.setLayout(config_layout)

        paths_group = QGroupBox("Маршрутизация файлов")
        paths_layout = QGridLayout()
        paths_layout.addWidget(QLabel("Открытый текст:"), 0, 0)
        paths_layout.addWidget(self.input_file_edit, 0, 1)
        paths_layout.addWidget(QLabel("Шифртекст:"), 1, 0)
        paths_layout.addWidget(self.encrypted_file_edit, 1, 1)
        paths_layout.addWidget(QLabel("Расшифрованный текст:"), 2, 0)
        paths_layout.addWidget(self.decrypted_file_edit, 2, 1)
        paths_layout.addWidget(QLabel("Шифр-ключ (AES):"), 3, 0)
        paths_layout.addWidget(self.encrypted_key_edit, 3, 1)
        paths_layout.addWidget(QLabel("Открытый ключ (RSA):"), 4, 0)
        paths_layout.addWidget(self.public_key_edit, 4, 1)
        paths_layout.addWidget(QLabel("Закрытый ключ (RSA):"), 5, 0)
        paths_layout.addWidget(self.private_key_edit, 5, 1)
        paths_group.setLayout(paths_layout)

        params_group = QGroupBox("Характеристики шифров")
        params_layout = QGridLayout()
        params_layout.addWidget(QLabel("Симметричный ключ (AES):"), 0, 0)
        params_layout.addWidget(self.aes_size_box, 0, 1)
        params_layout.addWidget(QLabel("бит"), 0, 2)
        params_layout.addWidget(QLabel("Асимметричный ключ (RSA):"), 1, 0)
        params_layout.addWidget(self.rsa_size_edit, 1, 1)
        params_layout.addWidget(QLabel("бит"), 1, 2)
        params_layout.addWidget(QLabel("Экспонента RSA:"), 2, 0)
        params_layout.addWidget(self.rsa_exponent_edit, 2, 1)
        params_group.setLayout(params_layout)

        settings_layout.addWidget(config_group)
        settings_layout.addWidget(paths_group)
        settings_layout.addWidget(params_group)
        settings_layout.addStretch()
        self.tab_settings.setLayout(settings_layout)

        operations_layout = QVBoxLayout()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.generate_button)
        buttons_layout.addWidget(self.encrypt_button)
        buttons_layout.addWidget(self.decrypt_button)
        
        log_group = QGroupBox("Журнал событий")
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_box)
        log_group.setLayout(log_layout)

        operations_layout.addLayout(buttons_layout)
        operations_layout.addWidget(log_group)
        self.tab_operations.setLayout(operations_layout)

    def connect_buttons(self) -> None:
        self.choose_config_button.clicked.connect(self.choose_config)
        self.load_config_button.clicked.connect(self.load_config)
        self.generate_button.clicked.connect(self.generate_keys_action)
        self.encrypt_button.clicked.connect(self.encrypt_file_action)
        self.decrypt_button.clicked.connect(self.decrypt_file_action)

    def set_styles(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #bac2de;
            }
            QGroupBox {
                border: 1px solid #45475a;
                border-radius: 6px;
                margin-top: 14px;
                padding-top: 10px;
                font-weight: bold;
                color: #89b4fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 4px;
                padding: 6px;
                color: #cdd6f4;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            QTabWidget::pane {
                border: 1px solid #45475a;
                border-radius: 4px;
                background-color: #1e1e2e;
            }
            QTabBar::tab {
                background: #313244;
                color: #a6adc8;
                padding: 8px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #89b4fa;
                color: #11111b;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background: #45475a;
            }
            """
        )
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #89b4fa; padding-bottom: 10px;")

    def try_load_from_args(self) -> None:
        match len(sys.argv) > 1:
            case True:
                self.config_path_edit.setText(sys.argv[1])
                self.load_config()
            case False:
                pass

    def choose_config(self) -> None:
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
        path = self.config_path_edit.text().strip()
        match path:
            case "":
                self.show_error(ValueError("Не указан путь к файлу настроек"))
                return
            case _:
                try:
                    self.settings = self._file_service.load_settings(path)
                    self.fill_settings_fields()
                    self.log(f"✅ Настройки успешно загружены: {path}")
                    self.tabs.setCurrentIndex(1)
                except ValueError as exc:
                    self.show_error(exc)

    def fill_settings_fields(self) -> None:
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
            raise KeyError(f"В settings.json отсутствует обязательный параметр: {exc}") from exc

    def get_checked_settings(self) -> dict:
        match self.settings is None:
            case True:
                raise RuntimeError("Пожалуйста, сначала загрузите файл настроек во вкладке 'Настройки'")
            case False:
                self.settings["aes_key_size"] = int(self.aes_size_box.currentText())
                return self.settings

    def generate_keys_action(self) -> None:
        try:
            settings = self.get_checked_settings()

            self.log("—" * 40)
            self.log("⏳ [1/3] Запуск генерации ключей...")
            self.log("🔑 Создание симметричного AES-ключа...")
            self.log("🔏 Создание асимметричной пары RSA-ключа...")

            self._crypto_system.run_key_generation(
                settings["encrypted_key_file"],
                settings["public_key_file"],
                settings["private_key_file"],
                settings["aes_key_size"],
                settings["rsa_key_size"],
                settings["rsa_public_exponent"],
            )

            self.log("🔒 AES-ключ зашифрован открытым RSA-ключом")
            self.log("💾 Ключи успешно сохранены на диск")
            self.show_info("Процесс генерации ключей завершен успешно!")
        except (RuntimeError, KeyError, HybridCryptoError) as exc:
            self.show_error(exc)

    def encrypt_file_action(self) -> None:
        try:
            settings = self.get_checked_settings()

            self.log("—" * 40)
            self.log("⏳ [2/3] Запуск шифрования файла...")
            self.log("🔓 Дешифрование AES-ключа с помощью закрытого RSA-ключа...")

            self._crypto_system.run_encryption(
                settings["input_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["encrypted_file"],
            )

            self.log(f"📁 Файл зашифрован и сохранен как: {settings['encrypted_file']}")
            self.show_info("Файл успешно зашифрован алгоритмом AES!")
        except (RuntimeError, KeyError, HybridCryptoError, ValueError) as exc:
            self.show_error(exc)

    def decrypt_file_action(self) -> None:
        try:
            settings = self.get_checked_settings()

            self.log("—" * 40)
            self.log("⏳ [3/3] Запуск дешифрования файла...")
            self.log("🔓 Дешифрование AES-ключа с помощью закрытого RSA-ключа...")

            self._crypto_system.run_decryption(
                settings["encrypted_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["decrypted_file"],
            )

            self.log(f"📄 Исходный файл восстановлен и сохранен как: {settings['decrypted_file']}")
            self.show_info("Файл успешно дешифрован. Данные восстановлены!")
        except (RuntimeError, KeyError, HybridCryptoError, ValueError) as exc:
            self.show_error(exc)

    def log(self, text: str) -> None:
        self.log_box.append(text)

    def show_error(self, error: Exception) -> None:
        self.log(f"❌ Ошибка: {error}")
        QMessageBox.critical(self, "Критическая ошибка", str(error))

    def show_info(self, text: str) -> None:
        QMessageBox.information(self, "Успех", text)