import sys
from PyQt5.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)
from typing import Optional, Dict, Any

from exceptions import HybridCryptoError
from file_utils import FileService
from hybrid import HybridCryptoSystem


class CryptoApp(QWidget):
    """Главное окно приложения с использованием вкладок (QTabWidget).
    
    Предоставляет графический интерфейс для управления гибридной криптосистемой.
    Состоит из двух основных вкладок:
    - Настройки и пути: загрузка конфигурации и настройка путей к файлам
    - Криптография и Журнал: выполнение операций и просмотр логов
    
    Attributes:
        settings (Optional[Dict[str, Any]]): Загруженные настройки конфигурации.
        _file_service (FileService): Сервис для работы с файлами.
        _crypto_system (HybridCryptoSystem): Экземпляр гибридной криптосистемы.
    """
    
    def __init__(self):
        """Инициализирует главное окно приложения.
        
        Создает все виджеты, настраивает layout, подключает сигналы,
        применяет стили и пытается загрузить конфигурацию из аргументов командной строки.
        """
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
        """Создает все графические компоненты интерфейса.
        
        Инициализирует:
        - Заголовок приложения
        - Вкладки (настройки и операции)
        - Поля для ввода путей к файлам
        - Выпадающие списки и поля для параметров шифрования
        - Кнопки для выполнения операций
        - Область для вывода логов
        """
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
        """Организует расположение всех виджетов в окне приложения.
        
        Создает иерархическую структуру layout для вкладок:
        - Вкладка настроек: группа конфигурации, группа путей, группа параметров
        - Вкладка операций: кнопки и журнал событий
        """
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
        params_layout.addWidget(QLabel("бит"), 1,
