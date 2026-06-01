import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox,
    QGridLayout, QMessageBox, QProgressBar, QTabWidget, QTextEdit,
    QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from hybrid import HybridCrypto
from utils import load_settings, save_settings


class CryptoWorker(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)

    def __init__(self, operation, params):
        super().__init__()
        self.operation = operation
        self.params = params
        self.crypto = HybridCrypto()

    def run(self):
        try:
            if self.operation == 'keys':
                self.progress.emit("Генерация ключей...")
                self.crypto.generate_keys(
                    self.params['public_path'],
                    self.params['private_path'],
                    self.params['encrypted_key_path'],
                    self.params['key_length']
                )
                self.finished.emit(True, "Ключи успешно созданы")
            
            elif self.operation == 'encrypt':
                self.progress.emit("Шифрование файла...")
                self.crypto.encrypt_file(
                    self.params['input_file'],
                    self.params['output_file'],
                    self.params['public_key_path'],
                    self.params['encrypted_key_path'],
                    self.params['key_length']
                )
                self.finished.emit(True, "Файл успешно зашифрован")
            
            elif self.operation == 'decrypt':
                self.progress.emit("Расшифровка файла...")
                self.crypto.decrypt_file(
                    self.params['input_file'],
                    self.params['output_file'],
                    self.params['private_key_path'],
                    self.params['encrypted_key_path']
                )
                self.finished.emit(True, "Файл успешно расшифрован")
                
        except Exception as e:
            self.finished.emit(False, str(e))


class CryptoApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.settings_file = "settings.json"
        self.settings = load_settings(self.settings_file)
        self.worker = None
        self.setup_ui()
        self.load_settings_to_ui()
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b36;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QGroupBox {
                color: #ffaa44;
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: #3a3a4a;
            }
            QLineEdit {
                padding: 6px;
                background-color: #4a4a5a;
                color: #ffffff;
                border: 1px solid #666;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #5a6a7a;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a7a8a;
            }
            QPushButton#generateBtn {
                background-color: #44aa66;
            }
            QPushButton#encryptBtn {
                background-color: #2288cc;
            }
            QPushButton#decryptBtn {
                background-color: #cc8822;
            }
            QTabWidget::pane {
                background-color: #3a3a4a;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #4a4a5a;
                color: #ddd;
                padding: 8px 20px;
                margin: 3px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #ffaa44;
                color: #2b2b36;
            }
            QTextEdit {
                background-color: #1e1e2a;
                color: #aaffaa;
                border: 1px solid #555;
                border-radius: 5px;
                font-family: monospace;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #44aa66;
                border-radius: 4px;
            }
        """)

    def setup_ui(self):
        self.setWindowTitle("Гибридная криптосистема RSA + Blowfish")
        self.setGeometry(150, 150, 950, 650)
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)

        self.create_header(layout)
        self.create_tabs(layout)
        self.create_statusbar()

    def create_header(self, parent_layout):
        header = QLabel("Гибридная криптосистема RSA + Blowfish")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ffaa44; padding: 15px;")
        parent_layout.addWidget(header)

        sub = QLabel("RSA-2048 | Blowfish CBC (ключ 32-448 бит)")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #ccccaa; font-size: 11px;")
        parent_layout.addWidget(sub)

    def create_tabs(self, parent_layout):
        self.tabs = QTabWidget()
        parent_layout.addWidget(self.tabs)

        self.create_keys_tab()
        self.create_encrypt_tab()
        self.create_decrypt_tab()
        self.create_log_tab()

    def create_keys_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Параметры генерации ключей")
        grid = QGridLayout(group)
        grid.setSpacing(12)

        grid.addWidget(QLabel("Открытый ключ RSA:"), 0, 0)
        self.le_public = QLineEdit()
        grid.addWidget(self.le_public, 0, 1)
        btn_pub = QPushButton("Обзор")
        btn_pub.clicked.connect(lambda: self.choose_file(self.le_public, save=True))
        grid.addWidget(btn_pub, 0, 2)

        grid.addWidget(QLabel("Закрытый ключ RSA:"), 1, 0)
        self.le_private = QLineEdit()
        grid.addWidget(self.le_private, 1, 1)
        btn_priv = QPushButton("Обзор")
        btn_priv.clicked.connect(lambda: self.choose_file(self.le_private, save=True))
        grid.addWidget(btn_priv, 1, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 2, 0)
        self.le_encrypted_key = QLineEdit()
        grid.addWidget(self.le_encrypted_key, 2, 1)
        btn_enc = QPushButton("Обзор")
        btn_enc.clicked.connect(lambda: self.choose_file(self.le_encrypted_key, save=True))
        grid.addWidget(btn_enc, 2, 2)

        grid.addWidget(QLabel("Длина ключа Blowfish (32-448, кратно 8):"), 3, 0)
        self.spin_keylen = QSpinBox()
        self.spin_keylen.setMinimum(32)
        self.spin_keylen.setMaximum(448)
        self.spin_keylen.setSingleStep(8)
        self.spin_keylen.setValue(128)
        self.spin_keylen.setStyleSheet("background-color: #4a4a5a; color: white;")
        grid.addWidget(self.spin_keylen, 3, 1)

        layout.addWidget(group)

        self.btn_generate = QPushButton("Сгенерировать ключи")
        self.btn_generate.setObjectName("generateBtn")
        self.btn_generate.clicked.connect(self.start_keygen)
        layout.addWidget(self.btn_generate)

        layout.addStretch()
        self.tabs.addTab(tab, "Генерация ключей")

    def create_encrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Параметры шифрования")
        grid = QGridLayout(group)
        grid.setSpacing(12)

        grid.addWidget(QLabel("Исходный файл:"), 0, 0)
        self.le_enc_in = QLineEdit()
        grid.addWidget(self.le_enc_in, 0, 1)
        btn_in = QPushButton("Обзор")
        btn_in.clicked.connect(lambda: self.choose_file(self.le_enc_in))
        grid.addWidget(btn_in, 0, 2)

        grid.addWidget(QLabel("Зашифрованный файл:"), 1, 0)
        self.le_enc_out = QLineEdit()
        grid.addWidget(self.le_enc_out, 1, 1)
        btn_out = QPushButton("Обзор")
        btn_out.clicked.connect(lambda: self.choose_file(self.le_enc_out, save=True))
        grid.addWidget(btn_out, 1, 2)

        # ИСПРАВЛЕНО: "Открытый ключ RSA" вместо "Закрытый ключ RSA"
        grid.addWidget(QLabel("Открытый ключ RSA:"), 2, 0)
        self.le_enc_pub = QLineEdit()
        grid.addWidget(self.le_enc_pub, 2, 1)
        btn_pub = QPushButton("Обзор")
        btn_pub.clicked.connect(lambda: self.choose_file(self.le_enc_pub))
        grid.addWidget(btn_pub, 2, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 3, 0)
        self.le_enc_sym = QLineEdit()
        grid.addWidget(self.le_enc_sym, 3, 1)
        btn_sym = QPushButton("Обзор")
        btn_sym.clicked.connect(lambda: self.choose_file(self.le_enc_sym))
        grid.addWidget(btn_sym, 3, 2)

        layout.addWidget(group)

        self.btn_encrypt = QPushButton("Зашифровать файл")
        self.btn_encrypt.setObjectName("encryptBtn")
        self.btn_encrypt.clicked.connect(self.start_encrypt)
        layout.addWidget(self.btn_encrypt)

        layout.addStretch()
        self.tabs.addTab(tab, "Шифрование")

    def create_decrypt_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Параметры расшифровки")
        grid = QGridLayout(group)
        grid.setSpacing(12)

        grid.addWidget(QLabel("Зашифрованный файл:"), 0, 0)
        self.le_dec_in = QLineEdit()
        grid.addWidget(self.le_dec_in, 0, 1)
        btn_in = QPushButton("Обзор")
        btn_in.clicked.connect(lambda: self.choose_file(self.le_dec_in))
        grid.addWidget(btn_in, 0, 2)

        grid.addWidget(QLabel("Расшифрованный файл:"), 1, 0)
        self.le_dec_out = QLineEdit()
        grid.addWidget(self.le_dec_out, 1, 1)
        btn_out = QPushButton("Обзор")
        btn_out.clicked.connect(lambda: self.choose_file(self.le_dec_out, save=True))
        grid.addWidget(btn_out, 1, 2)

        grid.addWidget(QLabel("Закрытый ключ RSA:"), 2, 0)
        self.le_dec_priv = QLineEdit()
        grid.addWidget(self.le_dec_priv, 2, 1)
        btn_priv = QPushButton("Обзор")
        btn_priv.clicked.connect(lambda: self.choose_file(self.le_dec_priv))
        grid.addWidget(btn_priv, 2, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 3, 0)
        self.le_dec_sym = QLineEdit()
        grid.addWidget(self.le_dec_sym, 3, 1)
        btn_sym = QPushButton("Обзор")
        btn_sym.clicked.connect(lambda: self.choose_file(self.le_dec_sym))
        grid.addWidget(btn_sym, 3, 2)

        layout.addWidget(group)

        self.btn_decrypt = QPushButton("Расшифровать файл")
        self.btn_decrypt.setObjectName("decryptBtn")
        self.btn_decrypt.clicked.connect(self.start_decrypt)
        layout.addWidget(self.btn_decrypt)

        layout.addStretch()
        self.tabs.addTab(tab, "Расшифровка")

    def create_log_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        btn_clear = QPushButton("Очистить лог")
        btn_clear.clicked.connect(self.log_area.clear)
        layout.addWidget(btn_clear)

        self.tabs.addTab(tab, "Лог операций")

    def create_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Готов к работе")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(180)
        self.progress_bar.setVisible(False)
        self.statusbar.addPermanentWidget(self.progress_bar)

    def choose_file(self, line_edit, save=False):
        if save:
            path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Все файлы (*.*)")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Все файлы (*.*)")
        if path:
            line_edit.setText(path)
            self.save_settings_to_file()

    def save_settings_to_file(self):
        settings = {
            'public_key': self.le_public.text(),
            'secret_key': self.le_private.text(),
            'symmetric_key': self.le_encrypted_key.text(),
            'symmetric_key_length': self.spin_keylen.value(),
            'enc_input': self.le_enc_in.text(),
            'enc_output': self.le_enc_out.text(),
            'enc_public': self.le_enc_pub.text(),
            'enc_sym': self.le_enc_sym.text(),
            'dec_input': self.le_dec_in.text(),
            'dec_output': self.le_dec_out.text(),
            'dec_private': self.le_dec_priv.text(),
            'dec_sym': self.le_dec_sym.text()
        }
        save_settings(settings, self.settings_file)

    def load_settings_to_ui(self):
        self.le_public.setText(self.settings.get('public_key', ''))
        self.le_private.setText(self.settings.get('secret_key', ''))
        self.le_encrypted_key.setText(self.settings.get('symmetric_key', ''))
        self.spin_keylen.setValue(self.settings.get('symmetric_key_length', 128))
        self.le_enc_in.setText(self.settings.get('enc_input', ''))
        self.le_enc_out.setText(self.settings.get('enc_output', ''))
        self.le_enc_pub.setText(self.settings.get('enc_public', ''))
        self.le_enc_sym.setText(self.settings.get('enc_sym', ''))
        self.le_dec_in.setText(self.settings.get('dec_input', ''))
        self.le_dec_out.setText(self.settings.get('dec_output', ''))
        self.le_dec_priv.setText(self.settings.get('dec_private', ''))
        self.le_dec_sym.setText(self.settings.get('dec_sym', ''))

    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")

    def set_controls_enabled(self, enabled):
        self.btn_generate.setEnabled(enabled)
        self.btn_encrypt.setEnabled(enabled)
        self.btn_decrypt.setEnabled(enabled)
        self.progress_bar.setVisible(not enabled)
        if not enabled:
            self.progress_bar.setRange(0, 0)
            self.statusbar.showMessage("Выполнение операции...")
        else:
            self.statusbar.showMessage("Готов к работе")

    def on_operation_finished(self, success, message):
        self.set_controls_enabled(True)
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.critical(self, "Ошибка", message)

    def start_keygen(self):
        if not all([self.le_public.text(), self.le_private.text(), self.le_encrypted_key.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните все пути для сохранения ключей")
            return
        
        klen = self.spin_keylen.value()
        if klen % 8 != 0:
            QMessageBox.warning(self, "Ошибка", "Длина ключа Blowfish должна быть кратна 8")
            return

        self.set_controls_enabled(False)
        self.worker = CryptoWorker('keys', {
            'public_path': self.le_public.text(),
            'private_path': self.le_private.text(),
            'encrypted_key_path': self.le_encrypted_key.text(),
            'key_length': klen
        })
        self.worker.progress.connect(self.add_log)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()

    def start_encrypt(self):
        if not all([self.le_enc_in.text(), self.le_enc_out.text(), 
                    self.le_enc_pub.text(), self.le_enc_sym.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if not os.path.exists(self.le_enc_in.text()):
            QMessageBox.warning(self, "Ошибка", "Исходный файл не найден")
            return

        self.set_controls_enabled(False)
        self.worker = CryptoWorker('encrypt', {
            'input_file': self.le_enc_in.text(),
            'output_file': self.le_enc_out.text(),
            'public_key_path': self.le_enc_pub.text(),
            'encrypted_key_path': self.le_enc_sym.text(),
            'key_length': self.spin_keylen.value()
        })
        self.worker.progress.connect(self.add_log)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()

    def start_decrypt(self):
        if not all([self.le_dec_in.text(), self.le_dec_out.text(),
                    self.le_dec_priv.text(), self.le_dec_sym.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if not os.path.exists(self.le_dec_in.text()):
            QMessageBox.warning(self, "Ошибка", "Зашифрованный файл не найден")
            return

        self.set_controls_enabled(False)
        self.worker = CryptoWorker('decrypt', {
            'input_file': self.le_dec_in.text(),
            'output_file': self.le_dec_out.text(),
            'private_key_path': self.le_dec_priv.text(),
            'encrypted_key_path': self.le_dec_sym.text()
        })
        self.worker.progress.connect(self.add_log)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()


def main():
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()