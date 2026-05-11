import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QMessageBox, QFileDialog, QLabel)
import keygen
import encrypt
import decrypt
import settings_loader

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_path = 'settings.json'
        self.current_settings = settings_loader.load(self.settings_path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hybrid Crypto System')
        self.setMinimumWidth(600)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>1. Управление ключами</b>"))
        
        btn_gen = QPushButton('Сгенерировать новые ключи (в папки по умолчанию)')
        btn_gen.clicked.connect(self.handle_keygen)
        layout.addWidget(btn_gen)

        self.btn_private = QPushButton(f"Приватный ключ RSA: {self.current_settings['private_key']}")
        self.btn_private.clicked.connect(lambda: self.select_path('private_key', "PEM Files (*.pem)"))
        
        self.btn_sym = QPushButton(f"Зашифрованный ключ AES: {self.current_settings['symmetric_key']}")
        self.btn_sym.clicked.connect(lambda: self.select_path('symmetric_key', "Binary Files (*.bin)"))

        layout.addWidget(self.btn_private)
        layout.addWidget(self.btn_sym)

        layout.addWidget(QLabel("<br><b>2. Выбор данных для обработки</b>"))
        
        self.btn_source = QPushButton(f"Исходный текст: {self.current_settings['initial_file']}")
        self.btn_source.clicked.connect(lambda: self.select_path('initial_file', "Text Files (*.txt);;All Files (*)"))
        
        self.btn_encrypted = QPushButton(f"Файл для сохранения шифра: {self.current_settings['encrypted_file']}")
        self.btn_encrypted.clicked.connect(lambda: self.select_save_path('encrypted_file', "Binary Files (*.bin)"))

        layout.addWidget(self.btn_source)
        layout.addWidget(self.btn_encrypted)

        layout.addWidget(QLabel("<br><b>3. Выполнение операций</b>"))
        btn_enc = QPushButton('Зашифровать выбранный файл')
        btn_enc.clicked.connect(self.handle_encryption)
        
        btn_dec = QPushButton('Расшифровать выбранный файл')
        btn_dec.clicked.connect(self.handle_decryption)
        
        layout.addWidget(btn_enc)
        layout.addWidget(btn_dec)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def select_path(self, key, file_filter):
        """Выбор существующего файла."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", file_filter)
        if file_path:
            self.update_setting(key, file_path)

    def select_save_path(self, key, file_filter):
        """Выбор пути для сохранения нового файла."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как...", "", file_filter)
        if file_path:
            self.update_setting(key, file_path)

    def update_setting(self, key, path):
        """Обновление внутренней конфигурации и текста кнопки."""
        self.current_settings[key] = path
        sender = self.sender()
        if sender:
            sender.setText(f"{key.replace('_', ' ').capitalize()}: {path}")
        self.log.append(f"[CONFIG]: Путь {key} изменен на {path}")

    def sync_settings(self):
        """Запись текущих путей в settings.json перед запуском модулей."""
        settings_loader.save(self.settings_path, self.current_settings)

    def handle_keygen(self):
        try:
            self.sync_settings()
            result = keygen.keygen(self.settings_path)
            self.log.append(f"[SUCCESS]: {result}")
        except Exception as e:
            self.show_error(e)

    def handle_encryption(self):
        try:
            self.sync_settings()
            result = encrypt.run_encryption(self.settings_path)
            self.log.append(f"[SUCCESS]: {result}")
        except Exception as e:
            self.show_error(e)

    def handle_decryption(self):
        try:
            self.sync_settings()
            result = decrypt.run_decryption(self.settings_path)
            self.log.append(f"[SUCCESS]: {result}")
        except Exception as e:
            self.show_error(e)

    def show_error(self, e):
        QMessageBox.critical(self, "Error", f"Ошибка: {str(e)}")
        self.log.append(f"[ERROR]: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CryptoApp()
    ex.show()
    sys.exit(app.exec_())