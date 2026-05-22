import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox,
    QGridLayout, QMessageBox, QProgressBar, QSpinBox,
    QTabWidget, QPlainTextEdit, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from crypto_hybrid import generate_hybrid_keys, encrypt_file, decrypt_file
from utils import handle_error, load_settings, save_settings


class WorkerThread(QThread):
    finished = pyqtSignal(bool, str)
    log = pyqtSignal(str)

    def __init__(self, operation, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs

    def run(self):
        try:
            if self.operation == 'generate':
                generate_hybrid_keys(
                    public_path=self.kwargs['public_path'],
                    secret_path=self.kwargs['secret_path'],
                    encrypted_sym_key_path=self.kwargs['encrypted_sym_path'],
                    sym_key_length=self.kwargs['key_length']
                )
                self.log.emit(f"[OK] Сгенерирован Blowfish ключ ({self.kwargs['key_length']} бит)")
                self.log.emit(f"[OK] Сгенерирована пара RSA ключей (2048 бит)")
                self.finished.emit(True, "Ключи успешно сгенерированы!")

            elif self.operation == 'encrypt':
                encrypt_file(
                    input_file=self.kwargs['input_file'],
                    output_file=self.kwargs['output_file'],
                    private_key_path=self.kwargs['private_key_path'],
                    encrypted_sym_key_path=self.kwargs['encrypted_sym_path']
                )
                self.log.emit(f"[OK] Файл зашифрован Blowfish: {self.kwargs['output_file']}")
                self.finished.emit(True, "Файл успешно зашифрован!")

            elif self.operation == 'decrypt':
                decrypt_file(
                    input_file=self.kwargs['input_file'],
                    output_file=self.kwargs['output_file'],
                    private_key_path=self.kwargs['private_key_path'],
                    encrypted_sym_key_path=self.kwargs['encrypted_sym_path']
                )
                self.log.emit(f"[OK] Файл расшифрован: {self.kwargs['output_file']}")
                self.finished.emit(True, "Файл успешно расшифрован!")

        except Exception as e:
            error_msg = handle_error(e, self.operation)
            self.log.emit(f"[ERROR] {error_msg}")
            self.finished.emit(False, error_msg)


class HybridCryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "app_settings.json"
        self.settings = load_settings(self.settings_file)
        self.worker = None
        self.init_ui()
        self.load_saved_paths()
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-size: 12px; }
            QGroupBox {
                color: #89b4fa; font-weight: bold; border: 2px solid #45475a;
                border-radius: 8px; margin-top: 10px; padding-top: 10px;
                background-color: #313244;
            }
            QLineEdit {
                padding: 6px; background-color: #45475a; color: #cdd6f4;
                border: 1px solid #585b70; border-radius: 5px;
            }
            QPushButton {
                background-color: #89b4fa; color: #1e1e2e; border: none;
                padding: 8px 16px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #b4befe; }
            QTabWidget::pane {
                border: 2px solid #45475a; border-radius: 8px;
                background-color: #313244;
            }
            QTabBar::tab {
                background-color: #45475a; color: #cdd6f4;
                padding: 8px 16px; margin: 2px; border-radius: 5px;
            }
            QTabBar::tab:selected { background-color: #89b4fa; color: #1e1e2e; }
            QPlainTextEdit {
                background-color: #1e1e2e; color: #a6e3a1;
                border: 1px solid #45475a; border-radius: 5px;
                font-family: Consolas;
            }
            QProgressBar {
                border: 1px solid #45475a; border-radius: 5px;
            }
            QProgressBar::chunk { background-color: #89b4fa; border-radius: 4px; }
            QSpinBox {
                background-color: #45475a; color: #cdd6f4;
                border: 1px solid #585b70; border-radius: 5px;
            }
        """)

    def init_ui(self):
        self.setWindowTitle("Гибридная криптосистема RSA + Blowfish")
        self.setGeometry(100, 100, 1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #89b4fa, stop:1 #b4befe);
                border-radius: 10px;
            }
        """)
        header.setFixedHeight(80)
        header_layout = QVBoxLayout(header)
        
        title = QLabel("ГИБРИДНАЯ КРИПТОСИСТЕМА")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e1e2e;")
        header_layout.addWidget(title)
        
        # ВОТ ЗДЕСЬ ИСПРАВЛЕНО - теперь Blowfish!
        subtitle = QLabel("RSA (2048 бит) + Blowfish (32-448 бит, режим CBC)")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #1e1e2e; font-size: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.setup_generation_tab()
        self.setup_encryption_tab()
        self.setup_decryption_tab()
        self.setup_log_tab()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress)

    def setup_generation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Генерация ключей Blowfish + RSA")
        grid = QGridLayout(group)
        grid.setVerticalSpacing(12)

        grid.addWidget(QLabel("Публичный RSA ключ:"), 0, 0)
        self.pub_key = QLineEdit()
        grid.addWidget(self.pub_key, 0, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.pub_key, save=True))
        grid.addWidget(btn, 0, 2)

        grid.addWidget(QLabel("Приватный RSA ключ:"), 1, 0)
        self.priv_key = QLineEdit()
        grid.addWidget(self.priv_key, 1, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.priv_key, save=True))
        grid.addWidget(btn, 1, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 2, 0)
        self.enc_key = QLineEdit()
        grid.addWidget(self.enc_key, 2, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.enc_key, save=True))
        grid.addWidget(btn, 2, 2)

        grid.addWidget(QLabel("Длина ключа Blowfish (32-448):"), 3, 0)
        self.key_len = QSpinBox()
        self.key_len.setMinimum(32)
        self.key_len.setMaximum(448)
        self.key_len.setSingleStep(8)
        self.key_len.setValue(128)
        grid.addWidget(self.key_len, 3, 1)

        self.gen_btn = QPushButton("СГЕНЕРИРОВАТЬ КЛЮЧИ (Blowfish + RSA)")
        self.gen_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.gen_btn.clicked.connect(self.generate_keys)
        grid.addWidget(self.gen_btn, 4, 0, 1, 3)

        layout.addWidget(group)
        layout.addStretch()
        self.tabs.addTab(tab, "Генерация")

    def setup_encryption_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Шифрование файла (Blowfish)")
        grid = QGridLayout(group)
        grid.setVerticalSpacing(12)

        grid.addWidget(QLabel("Исходный файл:"), 0, 0)
        self.enc_input = QLineEdit()
        grid.addWidget(self.enc_input, 0, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.enc_input))
        grid.addWidget(btn, 0, 2)

        grid.addWidget(QLabel("Зашифрованный файл:"), 1, 0)
        self.enc_output = QLineEdit()
        grid.addWidget(self.enc_output, 1, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.enc_output, save=True))
        grid.addWidget(btn, 1, 2)

        grid.addWidget(QLabel("Приватный RSA ключ:"), 2, 0)
        self.enc_priv = QLineEdit()
        grid.addWidget(self.enc_priv, 2, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.enc_priv))
        grid.addWidget(btn, 2, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 3, 0)
        self.enc_sym = QLineEdit()
        grid.addWidget(self.enc_sym, 3, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.enc_sym))
        grid.addWidget(btn, 3, 2)

        self.enc_btn = QPushButton("ЗАШИФРОВАТЬ ФАЙЛ (Blowfish)")
        self.enc_btn.setStyleSheet("background-color: #2196F3; color: white;")
        self.enc_btn.clicked.connect(self.encrypt_file)
        grid.addWidget(self.enc_btn, 4, 0, 1, 3)

        layout.addWidget(group)
        layout.addStretch()
        self.tabs.addTab(tab, "Шифрование")

    def setup_decryption_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Дешифрование файла (Blowfish)")
        grid = QGridLayout(group)
        grid.setVerticalSpacing(12)

        grid.addWidget(QLabel("Зашифрованный файл:"), 0, 0)
        self.dec_input = QLineEdit()
        grid.addWidget(self.dec_input, 0, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.dec_input))
        grid.addWidget(btn, 0, 2)

        grid.addWidget(QLabel("Расшифрованный файл:"), 1, 0)
        self.dec_output = QLineEdit()
        grid.addWidget(self.dec_output, 1, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.dec_output, save=True))
        grid.addWidget(btn, 1, 2)

        grid.addWidget(QLabel("Приватный RSA ключ:"), 2, 0)
        self.dec_priv = QLineEdit()
        grid.addWidget(self.dec_priv, 2, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.dec_priv))
        grid.addWidget(btn, 2, 2)

        grid.addWidget(QLabel("Зашифрованный ключ Blowfish:"), 3, 0)
        self.dec_sym = QLineEdit()
        grid.addWidget(self.dec_sym, 3, 1)
        btn = QPushButton("Обзор...")
        btn.clicked.connect(lambda: self.browse_file(self.dec_sym))
        grid.addWidget(btn, 3, 2)

        self.dec_btn = QPushButton("РАСШИФРОВАТЬ ФАЙЛ (Blowfish)")
        self.dec_btn.setStyleSheet("background-color: #FF9800; color: white;")
        self.dec_btn.clicked.connect(self.decrypt_file)
        grid.addWidget(self.dec_btn, 4, 0, 1, 3)

        layout.addWidget(group)
        layout.addStretch()
        self.tabs.addTab(tab, "Дешифрование")

    def setup_log_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        clear_btn = QPushButton("Очистить лог")
        clear_btn.clicked.connect(self.log_text.clear)
        layout.addWidget(clear_btn)
        
        self.tabs.addTab(tab, "Лог операций")

    def browse_file(self, line_edit, save=False):
        if save:
            path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Все файлы (*.*)")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Все файлы (*.*)")
        if path:
            line_edit.setText(path)
            self.save_current_paths()

    def save_current_paths(self):
        settings = {
            'public_key': self.pub_key.text(),
            'private_key': self.priv_key.text(),
            'encrypted_sym_key': self.enc_key.text(),
            'key_length': self.key_len.value(),
            'enc_input': self.enc_input.text(),
            'enc_output': self.enc_output.text(),
            'enc_private': self.enc_priv.text(),
            'enc_sym': self.enc_sym.text(),
            'dec_input': self.dec_input.text(),
            'dec_output': self.dec_output.text(),
            'dec_private': self.dec_priv.text(),
            'dec_sym': self.dec_sym.text(),
        }
        save_settings(settings, self.settings_file)

    def load_saved_paths(self):
        self.pub_key.setText(self.settings.get('public_key', ''))
        self.priv_key.setText(self.settings.get('private_key', ''))
        self.enc_key.setText(self.settings.get('encrypted_sym_key', ''))
        self.key_len.setValue(self.settings.get('key_length', 128))
        self.enc_input.setText(self.settings.get('enc_input', ''))
        self.enc_output.setText(self.settings.get('enc_output', ''))
        self.enc_priv.setText(self.settings.get('enc_private', ''))
        self.enc_sym.setText(self.settings.get('enc_sym', ''))
        self.dec_input.setText(self.settings.get('dec_input', ''))
        self.dec_output.setText(self.settings.get('dec_output', ''))
        self.dec_priv.setText(self.settings.get('dec_private', ''))
        self.dec_sym.setText(self.settings.get('dec_sym', ''))

    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.appendPlainText(f"[{timestamp}] {message}")

    def set_buttons_enabled(self, enabled):
        self.gen_btn.setEnabled(enabled)
        self.enc_btn.setEnabled(enabled)
        self.dec_btn.setEnabled(enabled)
        self.progress.setVisible(not enabled)
        if not enabled:
            self.progress.setRange(0, 0)
            self.status_bar.showMessage("Выполнение операции...")
        else:
            self.status_bar.showMessage("Готов к работе")

    def on_finished(self, success, message):
        self.set_buttons_enabled(True)
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.critical(self, "Ошибка", message)

    def generate_keys(self):
        if not self.pub_key.text() or not self.priv_key.text() or not self.enc_key.text():
            QMessageBox.warning(self, "Ошибка", "Заполните все пути для сохранения ключей")
            return
        
        self.set_buttons_enabled(False)
        self.worker = WorkerThread(
            operation='generate',
            public_path=self.pub_key.text(),
            secret_path=self.priv_key.text(),
            encrypted_sym_path=self.enc_key.text(),
            key_length=self.key_len.value()
        )
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def encrypt_file(self):
        if not all([self.enc_input.text(), self.enc_output.text(), 
                    self.enc_priv.text(), self.enc_sym.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        if not os.path.exists(self.enc_input.text()):
            QMessageBox.warning(self, "Ошибка", "Исходный файл не найден")
            return
        
        self.set_buttons_enabled(False)
        self.worker = WorkerThread(
            operation='encrypt',
            input_file=self.enc_input.text(),
            output_file=self.enc_output.text(),
            private_key_path=self.enc_priv.text(),
            encrypted_sym_path=self.enc_sym.text()
        )
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def decrypt_file(self):
        if not all([self.dec_input.text(), self.dec_output.text(),
                    self.dec_priv.text(), self.dec_sym.text()]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        
        if not os.path.exists(self.dec_input.text()):
            QMessageBox.warning(self, "Ошибка", "Зашифрованный файл не найден")
            return
        
        self.set_buttons_enabled(False)
        self.worker = WorkerThread(
            operation='decrypt',
            input_file=self.dec_input.text(),
            output_file=self.dec_output.text(),
            private_key_path=self.dec_priv.text(),
            encrypted_sym_path=self.dec_sym.text()
        )
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()


def main():
    app = QApplication(sys.argv)
    window = HybridCryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()