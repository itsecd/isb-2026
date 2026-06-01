import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QFileDialog, QMessageBox, QGroupBox,
                             QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from typing import Dict, Any, Optional
from datetime import datetime

import key_generation
import RSA
import text
import Camellia
import settings_manager


def normalize_path(path: str) -> str:
    """
    Нормализует путь для отображения и хранения.
    Преобразует обратные слеши в прямые для кроссплатформенности.
    
    Args:
        path (str): Исходный путь для нормализации
        
    Returns:
        str: Нормализованный путь с прямыми слешами
    """
    if isinstance(path, str):
        return path.replace('\\', '/')
    return path


class CryptoThread(QThread):
    """
    Поток для выполнения криптографических операций (шифрование/расшифрование).
    Позволяет не блокировать интерфейс при длительных операциях.
    """
    finished = pyqtSignal(bool, str)  
    progress = pyqtSignal(int)       

    def __init__(self, operation: str, **kwargs):
        """
        Инициализация потока криптографии.
        
        Args:
            operation (str): Тип операции ('encrypt' или 'decrypt')
            **kwargs: Параметры для операции:
                - text_file: путь к файлу с данными
                - symmetric_key: путь к зашифрованному симметричному ключу
                - private_key: путь к приватному ключу RSA
                - output_file: путь для сохранения результата
        """
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        
    def run(self) -> None:
        """
        Запуск операции в отдельном потоке.
        Вызывает соответствующий метод Camellia в зависимости от операции.
        """
        try:
            self.progress.emit(10)
            
            match self.operation:
                case 'encrypt':
                    Camellia.encrypt(
                        self.kwargs['text_file'],
                        self.kwargs['symmetric_key'],
                        self.kwargs['private_key'],
                        self.kwargs['output_file']
                    )
                case 'decrypt':
                    Camellia.decrypt(
                        self.kwargs['text_file'],
                        self.kwargs['symmetric_key'],
                        self.kwargs['private_key'],
                        self.kwargs['output_file']
                    )
                case _:
                    raise ValueError(f"Неизвестная операция: {self.operation}")
                    
            self.progress.emit(100)
            self.finished.emit(True, "Операция выполнена успешно!")
        except Exception as e:
            self.finished.emit(False, f"Ошибка: {str(e)}")


class KeyGenerationThread(QThread):
    """
    Поток для генерации ключей (RSA + симметричный ключ).
    Позволяет не блокировать интерфейс при генерации.
    """
    finished = pyqtSignal(bool, str) 
    
    def __init__(self, key_size: int, output_dir: str):
        """
        Инициализация потока генерации ключей.
        
        Args:
            key_size (int): Размер симметричного ключа в битах (128, 192 или 256)
            output_dir (str): Директория для сохранения ключей
        """
        super().__init__()
        self.key_size = key_size
        self.output_dir = normalize_path(output_dir)
        
    def run(self) -> None:
        """
        Запуск генерации ключей в отдельном потоке.
        Генерирует пару RSA ключей и симметричный ключ Camellia.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            private_key, public_key = key_generation.generate_asymmetric()
            
            private_path = normalize_path(os.path.join(self.output_dir, "private.pem"))
            public_path = normalize_path(os.path.join(self.output_dir, "public.pem"))
            
            RSA.serialize_private_key(private_key, private_path)
            RSA.serialize_public_key(public_key, public_path)
            
            symmetric_key = key_generation.generate_symmetric_key(self.key_size)
            
            encrypted_symmetric = key_generation.encrypt_symmetric_key(symmetric_key, public_key)
            
            symmetric_path = normalize_path(os.path.join(self.output_dir, "symmetric_encrypted.bin"))
            text.save_text(encrypted_symmetric, symmetric_path)
            
            self.finished.emit(True, f"Ключи успешно сгенерированы в папке: {self.output_dir}")
        except Exception as e:
            self.finished.emit(False, f"Ошибка генерации ключей: {str(e)}")


class HybridCryptoApp(QMainWindow):
    """
    Главное окно приложения гибридной криптосистемы (RSA + Camellia).
    Предоставляет интерфейс для генерации ключей, шифрования и расшифрования файлов.
    """
    
    def __init__(self, settings_file: Optional[str] = None):
        """
        Инициализация главного окна приложения.
        
        Args:
            settings_file (str, optional): Путь к файлу с настройками.
                                          Если None, используется путь по умолчанию.
        """
        super().__init__()
        if settings_file is None:
            settings_file = "settings.json"
        
        self.settings_file = normalize_path(settings_file)
        self.settings = self.load_settings()
        self.initUI()
        
    def load_settings(self) -> Dict[str, Any]:
        """
        Загрузка настроек из файла.
        
        Returns:
            Dict[str, Any]: Словарь с настройками приложения
            
        Note:
            Если файл настроек не найден, возвращаются значения по умолчанию
        """
        default_settings = {
            "initial_file": "data/source.txt",
            "encrypted_file": "data/encrypted.bin",
            "decrypted_file": "data/decrypted.txt",
            "symmetric_key": "keys/symmetric_encrypted.bin",
            "public_key": "keys/public.pem",
            "private_key": "keys/private.pem",
            "camellia_key_size": "128",
            "keys_directory": "keys"
        }
        
        try:
            if not os.path.exists(self.settings_file):
                self.log_message_to_console(f"Файл настроек не найден: {self.settings_file}")
                return default_settings.copy()
            
            settings = settings_manager.load(self.settings_file)

            for key in settings:
                if isinstance(settings[key], str) and key not in ["camellia_key_size"]:
                    settings[key] = normalize_path(settings[key])
            
            for key, default_value in default_settings.items():
                if key not in settings:
                    settings[key] = default_value
                    
            return settings
            
        except (FileNotFoundError, ValueError) as e:
            self.log_message_to_console(f"Ошибка загрузки настроек: {e}")
            return default_settings.copy()
    
    def log_message_to_console(self, message: str) -> None:
        """
        Вывод сообщения в консоль (для отладки).
        
        Args:
            message (str): Сообщение для вывода
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def save_settings(self) -> None:
        """Сохранение текущих настроек в файл."""
        try:
            settings_dir = os.path.dirname(self.settings_file)
            if settings_dir:
                os.makedirs(settings_dir, exist_ok=True)
            
            settings_manager.save(self.settings_file, self.settings)
            self.log(f"Настройки сохранены в {self.settings_file}")
        except Exception as e:
            QMessageBox.warning(self, "Предупреждение", f"Не удалось сохранить настройки: {e}")
            self.log(f"Ошибка сохранения настроек: {e}")
    
    def initUI(self) -> None:
        """
        Инициализация пользовательского интерфейса.
        Создает все виджеты и размещает их в окне.
        """
        self.setWindowTitle(f"Гибридная криптосистема (RSA + Camellia) - {self.settings_file}")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title = QLabel("Гибридная криптосистема")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        settings_info = QLabel(f"Файл настроек: {self.settings_file}")
        settings_info.setAlignment(Qt.AlignCenter)
        settings_info.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(settings_info)

        key_group = QGroupBox("Управление ключами")
        key_layout = QVBoxLayout()
        
        gen_layout = QHBoxLayout()
        gen_layout.addWidget(QLabel("Размер ключа Camellia:"))
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["128", "192", "256"])
        self.key_size_combo.setCurrentText(self.settings.get("camellia_key_size", "128"))
        gen_layout.addWidget(self.key_size_combo)
        
        self.gen_keys_btn = QPushButton("Сгенерировать новые ключи")
        self.gen_keys_btn.clicked.connect(self.generate_keys)
        gen_layout.addWidget(self.gen_keys_btn)
        
        self.keys_dir_edit = QLineEdit()
        self.keys_dir_edit.setPlaceholderText("Папка для сохранения ключей")
        default_keys_dir = self.settings.get("keys_directory", "keys")
        self.keys_dir_edit.setText(default_keys_dir)
        gen_layout.addWidget(self.keys_dir_edit)
        
        self.browse_keys_btn = QPushButton("Обзор")
        self.browse_keys_btn.clicked.connect(lambda: self.browse_folder(self.keys_dir_edit))
        gen_layout.addWidget(self.browse_keys_btn)
        
        key_layout.addLayout(gen_layout)
        
        key_info_layout = QHBoxLayout()
        self.public_key_label = QLabel("Публичный ключ: не выбран")
        self.private_key_label = QLabel("Приватный ключ: не выбран")
        key_info_layout.addWidget(self.public_key_label)
        key_info_layout.addWidget(self.private_key_label)
        key_layout.addLayout(key_info_layout)
        
        key_group.setLayout(key_layout)
        main_layout.addWidget(key_group)

        encrypt_group = QGroupBox("Шифрование")
        encrypt_layout = QVBoxLayout()
        
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Исходный файл:"))
        self.source_file_edit = QLineEdit()
        self.source_file_edit.setText(self.settings.get("initial_file", "data/source.txt"))
        source_layout.addWidget(self.source_file_edit)
        self.browse_source_btn = QPushButton("Обзор")
        self.browse_source_btn.clicked.connect(
            lambda: self.browse_file(self.source_file_edit, "Text files (*.txt);;All files (*.*)"))
        source_layout.addWidget(self.browse_source_btn)
        encrypt_layout.addLayout(source_layout)
        
        encrypted_layout = QHBoxLayout()
        encrypted_layout.addWidget(QLabel("Зашифрованный файл:"))
        self.encrypted_file_edit = QLineEdit()
        self.encrypted_file_edit.setText(self.settings.get("encrypted_file", "data/encrypted.bin"))
        encrypted_layout.addWidget(self.encrypted_file_edit)
        self.browse_encrypted_btn = QPushButton("Обзор")
        self.browse_encrypted_btn.clicked.connect(
            lambda: self.save_file(self.encrypted_file_edit, "Binary files (*.bin);;All files (*.*)"))
        encrypted_layout.addWidget(self.browse_encrypted_btn)
        encrypt_layout.addLayout(encrypted_layout)
        
        sym_key_layout = QHBoxLayout()
        sym_key_layout.addWidget(QLabel("Симметричный ключ (зашифр.):"))
        self.sym_key_edit = QLineEdit()
        self.sym_key_edit.setText(self.settings.get("symmetric_key", "keys/symmetric_encrypted.bin"))
        sym_key_layout.addWidget(self.sym_key_edit)
        self.browse_sym_btn = QPushButton("Обзор")
        self.browse_sym_btn.clicked.connect(
            lambda: self.browse_file(self.sym_key_edit, "All files (*.*)"))
        sym_key_layout.addWidget(self.browse_sym_btn)
        encrypt_layout.addLayout(sym_key_layout)
        
        priv_layout = QHBoxLayout()
        priv_layout.addWidget(QLabel("Приватный ключ RSA:"))
        self.priv_key_encrypt_edit = QLineEdit()
        self.priv_key_encrypt_edit.setText(self.settings.get("private_key", "keys/private.pem"))
        priv_layout.addWidget(self.priv_key_encrypt_edit)
        self.browse_priv_encrypt_btn = QPushButton("Обзор")
        self.browse_priv_encrypt_btn.clicked.connect(
            lambda: self.browse_file(self.priv_key_encrypt_edit, "PEM files (*.pem);;All files (*.*)"))
        priv_layout.addWidget(self.browse_priv_encrypt_btn)
        encrypt_layout.addLayout(priv_layout)
        
        self.encrypt_btn = QPushButton("Зашифровать файл")
        self.encrypt_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        encrypt_layout.addWidget(self.encrypt_btn)
        
        encrypt_group.setLayout(encrypt_layout)
        main_layout.addWidget(encrypt_group)

        decrypt_group = QGroupBox("Расшифрование")
        decrypt_layout = QVBoxLayout()
        
        enc_for_decrypt_layout = QHBoxLayout()
        enc_for_decrypt_layout.addWidget(QLabel("Зашифрованный файл:"))
        self.enc_for_decrypt_edit = QLineEdit()
        self.enc_for_decrypt_edit.setText(self.settings.get("encrypted_file", "data/encrypted.bin"))
        enc_for_decrypt_layout.addWidget(self.enc_for_decrypt_edit)
        self.browse_enc_decrypt_btn = QPushButton("Обзор")
        self.browse_enc_decrypt_btn.clicked.connect(
            lambda: self.browse_file(self.enc_for_decrypt_edit, "Binary files (*.bin);;All files (*.*)"))
        enc_for_decrypt_layout.addWidget(self.browse_enc_decrypt_btn)
        decrypt_layout.addLayout(enc_for_decrypt_layout)
        
        decrypted_layout = QHBoxLayout()
        decrypted_layout.addWidget(QLabel("Расшифрованный файл:"))
        self.decrypted_file_edit = QLineEdit()
        self.decrypted_file_edit.setText(self.settings.get("decrypted_file", "data/decrypted.txt"))
        decrypted_layout.addWidget(self.decrypted_file_edit)
        self.browse_decrypted_btn = QPushButton("Обзор")
        self.browse_decrypted_btn.clicked.connect(
            lambda: self.save_file(self.decrypted_file_edit, "Text files (*.txt);;All files (*.*)"))
        decrypted_layout.addWidget(self.browse_decrypted_btn)
        decrypt_layout.addLayout(decrypted_layout)
        
        sym_key_decrypt_layout = QHBoxLayout()
        sym_key_decrypt_layout.addWidget(QLabel("Симметричный ключ (зашифр.):"))
        self.sym_key_decrypt_edit = QLineEdit()
        self.sym_key_decrypt_edit.setText(self.settings.get("symmetric_key", "keys/symmetric_encrypted.bin"))
        sym_key_decrypt_layout.addWidget(self.sym_key_decrypt_edit)
        self.browse_sym_decrypt_btn = QPushButton("Обзор")
        self.browse_sym_decrypt_btn.clicked.connect(
            lambda: self.browse_file(self.sym_key_decrypt_edit, "All files (*.*)"))
        sym_key_decrypt_layout.addWidget(self.browse_sym_decrypt_btn)
        decrypt_layout.addLayout(sym_key_decrypt_layout)
        
        priv_decrypt_layout = QHBoxLayout()
        priv_decrypt_layout.addWidget(QLabel("Приватный ключ RSA:"))
        self.priv_key_decrypt_edit = QLineEdit()
        self.priv_key_decrypt_edit.setText(self.settings.get("private_key", "keys/private.pem"))
        priv_decrypt_layout.addWidget(self.priv_key_decrypt_edit)
        self.browse_priv_decrypt_btn = QPushButton("Обзор")
        self.browse_priv_decrypt_btn.clicked.connect(
            lambda: self.browse_file(self.priv_key_decrypt_edit, "PEM files (*.pem);;All files (*.*)"))
        priv_decrypt_layout.addWidget(self.browse_priv_decrypt_btn)
        decrypt_layout.addLayout(priv_decrypt_layout)
        
        self.decrypt_btn = QPushButton("Расшифровать файл")
        self.decrypt_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.decrypt_btn.clicked.connect(self.decrypt_file)
        decrypt_layout.addWidget(self.decrypt_btn)
        
        decrypt_group.setLayout(decrypt_layout)
        main_layout.addWidget(decrypt_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        log_group = QGroupBox("Лог операций")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        save_settings_btn = QPushButton("Сохранить настройки")
        save_settings_btn.clicked.connect(self.save_current_settings)
        main_layout.addWidget(save_settings_btn)
        
        self.statusBar().showMessage("Готов")
        
        os.makedirs("data", exist_ok=True)
        os.makedirs(self.keys_dir_edit.text(), exist_ok=True)
        
        self.log(f"Приложение запущено. Файл настроек: {self.settings_file}")
    
    def browse_file(self, line_edit: QLineEdit, file_filter: str) -> None:
        """
        Открытие диалога выбора файла.
        
        Args:
            line_edit (QLineEdit): Поле для отображения выбранного пути
            file_filter (str): Фильтр типов файлов
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        if file_path:
            normalized_path = normalize_path(file_path)
            line_edit.setText(normalized_path)
    
    def save_file(self, line_edit: QLineEdit, file_filter: str) -> None:
        """
        Открытие диалога сохранения файла.
        
        Args:
            line_edit (QLineEdit): Поле для отображения выбранного пути
            file_filter (str): Фильтр типов файлов
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", file_filter)
        if file_path:
            normalized_path = normalize_path(file_path)
            line_edit.setText(normalized_path)
    
    def browse_folder(self, line_edit: QLineEdit) -> None:
        """
        Открытие диалога выбора папки.
        
        Args:
            line_edit (QLineEdit): Поле для отображения выбранного пути
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            normalized_path = normalize_path(folder_path)
            line_edit.setText(normalized_path)
    
    def log(self, message: str) -> None:
        """
        Добавление сообщения в лог с временной меткой.
        
        Args:
            message (str): Сообщение для добавления в лог
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def generate_keys(self) -> None:
        """Запуск процесса генерации ключей в отдельном потоке."""
        key_size = int(self.key_size_combo.currentText())
        output_dir = normalize_path(self.keys_dir_edit.text())
        
        if not output_dir:
            QMessageBox.warning(self, "Предупреждение", "Укажите папку для сохранения ключей")
            return
        
        self.gen_keys_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.key_thread = KeyGenerationThread(key_size, output_dir)
        self.key_thread.finished.connect(self.on_keys_generated)
        self.key_thread.start()
        
        self.log(f"Начата генерация ключей (размер Camellia: {key_size} бит)")
    
    def on_keys_generated(self, success: bool, message: str) -> None:
        """
        Обработка завершения генерации ключей.
        
        Args:
            success (bool): Флаг успешности операции
            message (str): Сообщение о результате
        """
        self.gen_keys_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Успех", message)
            self.log(message)
            
            output_dir = normalize_path(self.keys_dir_edit.text())
            private_path = normalize_path(os.path.join(output_dir, "private.pem"))
            symmetric_path = normalize_path(os.path.join(output_dir, "symmetric_encrypted.bin"))
            
            self.priv_key_encrypt_edit.setText(private_path)
            self.priv_key_decrypt_edit.setText(private_path)
            self.sym_key_edit.setText(symmetric_path)
            self.sym_key_decrypt_edit.setText(symmetric_path)
            
            self.settings["private_key"] = private_path
            self.settings["public_key"] = normalize_path(os.path.join(output_dir, "public.pem"))
            self.settings["symmetric_key"] = symmetric_path
            self.settings["keys_directory"] = output_dir
            self.save_settings()
            
            self.public_key_label.setText(f"Публичный ключ: {normalize_path(os.path.join(output_dir, 'public.pem'))}")
            self.private_key_label.setText(f"Приватный ключ: {private_path}")
        else:
            QMessageBox.critical(self, "Ошибка", message)
            self.log(f"Ошибка: {message}")
    
    def encrypt_file(self) -> None:
        """Запуск процесса шифрования файла в отдельном потоке."""
        text_file = normalize_path(self.source_file_edit.text())
        sym_key = normalize_path(self.sym_key_edit.text())
        priv_key = normalize_path(self.priv_key_encrypt_edit.text())
        output_file = normalize_path(self.encrypted_file_edit.text())
        
        if not os.path.exists(text_file):
            QMessageBox.warning(self, "Предупреждение", f"Исходный файл не найден: {text_file}")
            return
        
        if not os.path.exists(sym_key):
            QMessageBox.warning(self, "Предупреждение", 
                               f"Файл симметричного ключа не найден: {sym_key}\nСначала сгенерируйте ключи.")
            return
        
        if not os.path.exists(priv_key):
            QMessageBox.warning(self, "Предупреждение", 
                               f"Приватный ключ не найден: {priv_key}\nСначала сгенерируйте ключи.")
            return
        
        self.encrypt_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.crypto_thread = CryptoThread(
            operation='encrypt',
            text_file=text_file,
            symmetric_key=sym_key,
            private_key=priv_key,
            output_file=output_file
        )
        self.crypto_thread.progress.connect(self.progress_bar.setValue)
        self.crypto_thread.finished.connect(self.on_encrypt_finished)
        self.crypto_thread.start()
        
        self.log(f"Начато шифрование файла: {text_file}")
    
    def on_encrypt_finished(self, success: bool, message: str) -> None:
        """
        Обработка завершения шифрования.
        
        Args:
            success (bool): Флаг успешности операции
            message (str): Сообщение о результате
        """
        self.encrypt_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Успех", message)
            self.log(message)
            self.statusBar().showMessage("Файл успешно зашифрован")
        else:
            QMessageBox.critical(self, "Ошибка", message)
            self.log(f"Ошибка: {message}")
            self.statusBar().showMessage("Ошибка шифрования")
    
    def decrypt_file(self) -> None:
        """Запуск процесса расшифрования файла в отдельном потоке."""
        text_file = normalize_path(self.enc_for_decrypt_edit.text())
        sym_key = normalize_path(self.sym_key_decrypt_edit.text())
        priv_key = normalize_path(self.priv_key_decrypt_edit.text())
        output_file = normalize_path(self.decrypted_file_edit.text())
        
        if not os.path.exists(text_file):
            QMessageBox.warning(self, "Предупреждение", f"Зашифрованный файл не найден: {text_file}")
            return
        
        if not os.path.exists(sym_key):
            QMessageBox.warning(self, "Предупреждение", f"Файл симметричного ключа не найден: {sym_key}")
            return
        
        if not os.path.exists(priv_key):
            QMessageBox.warning(self, "Предупреждение", f"Приватный ключ не найден: {priv_key}")
            return
        
        self.decrypt_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.crypto_thread = CryptoThread(
            operation='decrypt',
            text_file=text_file,
            symmetric_key=sym_key,
            private_key=priv_key,
            output_file=output_file
        )
        self.crypto_thread.progress.connect(self.progress_bar.setValue)
        self.crypto_thread.finished.connect(self.on_decrypt_finished)
        self.crypto_thread.start()
        
        self.log(f"Начато расшифрование файла: {text_file}")
    
    def on_decrypt_finished(self, success: bool, message: str) -> None:
        """
        Обработка завершения расшифрования.
        
        Args:
            success (bool): Флаг успешности операции
            message (str): Сообщение о результате
        """
        self.decrypt_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Успех", message)
            self.log(message)
            self.statusBar().showMessage("Файл успешно расшифрован")
        else:
            QMessageBox.critical(self, "Ошибка", message)
            self.log(f"Ошибка: {message}")
            self.statusBar().showMessage("Ошибка расшифрования")
    
    def save_current_settings(self) -> None:
        """Сохранение текущих настроек интерфейса в файл настроек."""
        self.settings["initial_file"] = normalize_path(self.source_file_edit.text())
        self.settings["encrypted_file"] = normalize_path(self.encrypted_file_edit.text())
        self.settings["decrypted_file"] = normalize_path(self.decrypted_file_edit.text())
        self.settings["symmetric_key"] = normalize_path(self.sym_key_edit.text())
        self.settings["private_key"] = normalize_path(self.priv_key_encrypt_edit.text())
        self.settings["camellia_key_size"] = self.key_size_combo.currentText()
        self.settings["keys_directory"] = normalize_path(self.keys_dir_edit.text())
        
        self.save_settings()
        QMessageBox.information(self, "Успех", "Настройки сохранены")
        self.log("Настройки сохранены")


def main(settings_file: Optional[str] = None) -> int:
    """
    Главная функция запуска приложения.
    
    Args:
        settings_file (str, optional): Путь к файлу с настройками.
                                      Если None, используется "settings.json".
    
    Returns:
        int: Код возврата приложения
    """
    app = QApplication(sys.argv)
    app.setApplicationName("HybridCrypto")
    
    os.makedirs("data", exist_ok=True)
    
    window = HybridCryptoApp(settings_file=settings_file)
    window.show()
    
    return sys.exit(app.exec_())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()