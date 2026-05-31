import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QFileDialog, QMessageBox, QGroupBox,
                             QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

import key_generation
import RSA
import symmetric
import Camellia
import settings_manager


def normalize_path(path):
    """
    Нормализует путь для отображения и хранения
    Преобразует обратные слеши в прямые для кроссплатформенности
    """
    if isinstance(path, str):
        return path.replace('\\', '/')
    return path


class CryptoThread(QThread):
    """Поток для выполнения криптографических операций"""
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)
    
    def __init__(self, operation, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        
    def run(self):
        try:
            self.progress.emit(10)
            if self.operation == 'encrypt':
                Camellia.encrypt(
                    self.kwargs['text_file'],
                    self.kwargs['symmetric_key'],
                    self.kwargs['private_key'],
                    self.kwargs['output_file']
                )
            elif self.operation == 'decrypt':
                Camellia.decrypt(
                    self.kwargs['text_file'],
                    self.kwargs['symmetric_key'],
                    self.kwargs['private_key'],
                    self.kwargs['output_file']
                )
            self.progress.emit(100)
            self.finished.emit(True, "Операция выполнена успешно!")
        except Exception as e:
            self.finished.emit(False, f"Ошибка: {str(e)}")


class KeyGenerationThread(QThread):
    """Поток для генерации ключей"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, key_size, output_dir):
        super().__init__()
        self.key_size = key_size
        self.output_dir = normalize_path(output_dir)
        
    def run(self):
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
            symmetric.serialize_symmetric_key(encrypted_symmetric, symmetric_path)
            
            self.finished.emit(True, f"Ключи успешно сгенерированы в папке: {self.output_dir}")
        except Exception as e:
            self.finished.emit(False, f"Ошибка генерации ключей: {str(e)}")


class HybridCryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.initUI()
        
    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            settings = settings_manager.load("settings.json")
            for key in ['initial_file', 'encrypted_file', 'decrypted_file', 
                       'symmetric_key', 'public_key', 'private_key']:
                if key in settings and isinstance(settings[key], str):
                    settings[key] = normalize_path(settings[key])
            return settings
        except:
            return {
                "initial_file": "data/source.txt",
                "encrypted_file": "data/encrypted.bin",
                "decrypted_file": "data/decrypted.txt",
                "symmetric_key": "keys/symmetric_encrypted.bin",
                "public_key": "keys/public.pem",
                "private_key": "keys/private.pem",
                "camellia_key_size": "128"
            }
    
    def save_settings(self):
        """Сохранение настроек"""
        try:
            settings_manager.save("settings.json", self.settings)
        except Exception as e:
            QMessageBox.warning(self, "Предупреждение", f"Не удалось сохранить настройки: {e}")
    
    def initUI(self):
        self.setWindowTitle("Гибридная криптосистема (RSA + Camellia)")
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
        self.keys_dir_edit.setText("keys")
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
        self.browse_source_btn.clicked.connect(lambda: self.browse_file(self.source_file_edit, "Text files (*.txt);;All files (*.*)"))
        source_layout.addWidget(self.browse_source_btn)
        encrypt_layout.addLayout(source_layout)
        
        encrypted_layout = QHBoxLayout()
        encrypted_layout.addWidget(QLabel("Зашифрованный файл:"))
        self.encrypted_file_edit = QLineEdit()
        self.encrypted_file_edit.setText(self.settings.get("encrypted_file", "data/encrypted.bin"))
        encrypted_layout.addWidget(self.encrypted_file_edit)
        self.browse_encrypted_btn = QPushButton("Обзор")
        self.browse_encrypted_btn.clicked.connect(lambda: self.save_file(self.encrypted_file_edit, "Binary files (*.bin);;All files (*.*)"))
        encrypted_layout.addWidget(self.browse_encrypted_btn)
        encrypt_layout.addLayout(encrypted_layout)
        
        sym_key_layout = QHBoxLayout()
        sym_key_layout.addWidget(QLabel("Симметричный ключ (зашифр.):"))
        self.sym_key_edit = QLineEdit()
        self.sym_key_edit.setText(self.settings.get("symmetric_key", "keys/symmetric_encrypted.bin"))
        sym_key_layout.addWidget(self.sym_key_edit)
        self.browse_sym_btn = QPushButton("Обзор")
        self.browse_sym_btn.clicked.connect(lambda: self.browse_file(self.sym_key_edit, "All files (*.*)"))
        sym_key_layout.addWidget(self.browse_sym_btn)
        encrypt_layout.addLayout(sym_key_layout)
        
        priv_layout = QHBoxLayout()
        priv_layout.addWidget(QLabel("Приватный ключ RSA:"))
        self.priv_key_encrypt_edit = QLineEdit()
        self.priv_key_encrypt_edit.setText(self.settings.get("private_key", "keys/private.pem"))
        priv_layout.addWidget(self.priv_key_encrypt_edit)
        self.browse_priv_encrypt_btn = QPushButton("Обзор")
        self.browse_priv_encrypt_btn.clicked.connect(lambda: self.browse_file(self.priv_key_encrypt_edit, "PEM files (*.pem);;All files (*.*)"))
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
        self.browse_enc_decrypt_btn.clicked.connect(lambda: self.browse_file(self.enc_for_decrypt_edit, "Binary files (*.bin);;All files (*.*)"))
        enc_for_decrypt_layout.addWidget(self.browse_enc_decrypt_btn)
        decrypt_layout.addLayout(enc_for_decrypt_layout)
        
        decrypted_layout = QHBoxLayout()
        decrypted_layout.addWidget(QLabel("Расшифрованный файл:"))
        self.decrypted_file_edit = QLineEdit()
        self.decrypted_file_edit.setText(self.settings.get("decrypted_file", "data/decrypted.txt"))
        decrypted_layout.addWidget(self.decrypted_file_edit)
        self.browse_decrypted_btn = QPushButton("Обзор")
        self.browse_decrypted_btn.clicked.connect(lambda: self.save_file(self.decrypted_file_edit, "Text files (*.txt);;All files (*.*)"))
        decrypted_layout.addWidget(self.browse_decrypted_btn)
        decrypt_layout.addLayout(decrypted_layout)
        
        sym_key_decrypt_layout = QHBoxLayout()
        sym_key_decrypt_layout.addWidget(QLabel("Симметричный ключ (зашифр.):"))
        self.sym_key_decrypt_edit = QLineEdit()
        self.sym_key_decrypt_edit.setText(self.settings.get("symmetric_key", "keys/symmetric_encrypted.bin"))
        sym_key_decrypt_layout.addWidget(self.sym_key_decrypt_edit)
        self.browse_sym_decrypt_btn = QPushButton("Обзор")
        self.browse_sym_decrypt_btn.clicked.connect(lambda: self.browse_file(self.sym_key_decrypt_edit, "All files (*.*)"))
        sym_key_decrypt_layout.addWidget(self.browse_sym_decrypt_btn)
        decrypt_layout.addLayout(sym_key_decrypt_layout)
        
        priv_decrypt_layout = QHBoxLayout()
        priv_decrypt_layout.addWidget(QLabel("Приватный ключ RSA:"))
        self.priv_key_decrypt_edit = QLineEdit()
        self.priv_key_decrypt_edit.setText(self.settings.get("private_key", "keys/private.pem"))
        priv_decrypt_layout.addWidget(self.priv_key_decrypt_edit)
        self.browse_priv_decrypt_btn = QPushButton("Обзор")
        self.browse_priv_decrypt_btn.clicked.connect(lambda: self.browse_file(self.priv_key_decrypt_edit, "PEM files (*.pem);;All files (*.*)"))
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
        os.makedirs("keys", exist_ok=True)
        
        self.log("Приложение запущено")
    
    def browse_file(self, line_edit, file_filter):
        """Выбор файла с нормализацией пути"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        if file_path:
            normalized_path = normalize_path(file_path)
            line_edit.setText(normalized_path)
    
    def save_file(self, line_edit, file_filter):
        """Выбор пути для сохранения файла с нормализацией"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", file_filter)
        if file_path:
            normalized_path = normalize_path(file_path)
            line_edit.setText(normalized_path)
    
    def browse_folder(self, line_edit):
        """Выбор папки с нормализацией"""
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            normalized_path = normalize_path(folder_path)
            line_edit.setText(normalized_path)
    
    def log(self, message):
        """Добавление сообщения в лог"""
        self.log_text.append(f"[{QApplication.instance().applicationDisplayName}] {message}")
    
    def generate_keys(self):
        """Генерация ключей"""
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
    
    def on_keys_generated(self, success, message):
        """Обработка завершения генерации ключей"""
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
            self.save_settings()
            
            self.public_key_label.setText(f"Публичный ключ: {normalize_path(os.path.join(output_dir, 'public.pem'))}")
            self.private_key_label.setText(f"Приватный ключ: {private_path}")
        else:
            QMessageBox.critical(self, "Ошибка", message)
            self.log(f"Ошибка: {message}")
    
    def encrypt_file(self):
        """Шифрование файла"""
        text_file = normalize_path(self.source_file_edit.text())
        sym_key = normalize_path(self.sym_key_edit.text())
        priv_key = normalize_path(self.priv_key_encrypt_edit.text())
        output_file = normalize_path(self.encrypted_file_edit.text())
        
        if not os.path.exists(text_file):
            QMessageBox.warning(self, "Предупреждение", f"Исходный файл не найден: {text_file}")
            return
        
        if not os.path.exists(sym_key):
            QMessageBox.warning(self, "Предупреждение", f"Файл симметричного ключа не найден: {sym_key}\nСначала сгенерируйте ключи.")
            return
        
        if not os.path.exists(priv_key):
            QMessageBox.warning(self, "Предупреждение", f"Приватный ключ не найден: {priv_key}\nСначала сгенерируйте ключи.")
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
    
    def on_encrypt_finished(self, success, message):
        """Обработка завершения шифрования"""
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
    
    def decrypt_file(self):
        """Расшифрование файла"""
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
    
    def on_decrypt_finished(self, success, message):
        """Обработка завершения расшифрования"""
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
    
    def save_current_settings(self):
        """Сохранение текущих настроек"""
        self.settings["initial_file"] = normalize_path(self.source_file_edit.text())
        self.settings["encrypted_file"] = normalize_path(self.encrypted_file_edit.text())
        self.settings["decrypted_file"] = normalize_path(self.decrypted_file_edit.text())
        self.settings["symmetric_key"] = normalize_path(self.sym_key_edit.text())
        self.settings["private_key"] = normalize_path(self.priv_key_encrypt_edit.text())
        self.settings["camellia_key_size"] = self.key_size_combo.currentText()
        
        self.save_settings()
        QMessageBox.information(self, "Успех", "Настройки сохранены")
        self.log("Настройки сохранены")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HybridCrypto")
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("keys", exist_ok=True)
    
    window = HybridCryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()