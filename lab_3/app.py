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

from crypto_hybrid import encrypt_data, decrypt_data, get_symmetric_key
from crypto_symmetric import generate_blowfish_key
from crypto_asymmetric import generate_key_pair, save_public_key, save_private_key, encrypt_rsa
from utils import write_bytes, read_bytes, load_settings, save_settings, FileUtilsError


class WorkerThread(QThread):
    """
    Поток для выполнения длительных криптографических операций без блокировки GUI.
    """
    finished = pyqtSignal(bool, str)
    log = pyqtSignal(str)

    def __init__(self, operation, **kwargs):
        """
        Инициализирует рабочий поток с указанной операцией и параметрами.
        
        Args:
            operation (str): Тип операции ('generate', 'encrypt', 'decrypt')
            **kwargs: Параметры для выполнения операции
        """
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs

    def run(self):
        """
        Выполняет операцию в отдельном потоке.
        """
        try:
            if self.operation == 'generate':
                self._generate_keys()
            elif self.operation == 'encrypt':
                self._encrypt_file()
            elif self.operation == 'decrypt':
                self._decrypt_file()
        except Exception as e:
            self.log.emit(f"[ОШИБКА] {str(e)}")
            self.finished.emit(False, str(e))

    def _generate_keys(self):
        """
        Генерирует пару RSA ключей и симметричный ключ Blowfish.
        """
        key_length = self.kwargs['key_length']
        self.log.emit(f"[INFO] Генерация Blowfish ключа длиной {key_length} бит")
        symmetric_key = generate_blowfish_key(key_length)
        
        self.log.emit(f"[INFO] Генерация пары ключей RSA длиной 2048 бит")
        private_key, public_key = generate_key_pair()
        
        save_private_key(self.kwargs['secret_path'], private_key)
        save_public_key(self.kwargs['public_path'], public_key)
        
        encrypted_symmetric_key = encrypt_rsa(public_key, symmetric_key)
        write_bytes(self.kwargs['encrypted_sym_path'], encrypted_symmetric_key)
        
        self.log.emit(f"[OK] Ключи успешно сгенерированы и сохранены")
        self.finished.emit(True, "Ключи успешно сгенерированы!")

    def _encrypt_file(self):
        """
        Шифрует файл с использованием гибридной схемы.
        """
        self.log.emit(f"[INFO] Чтение зашифрованного симметричного ключа")
        encrypted_sym_key = read_bytes(self.kwargs['encrypted_sym_path'])
        
        self.log.emit(f"[INFO] Загрузка приватного ключа RSA")
        from crypto_asymmetric import load_private_key
        private_key = load_private_key(self.kwargs['private_key_path'])
        
        self.log.emit(f"[INFO] Расшифровка симметричного ключа через RSA")
        from crypto_asymmetric import decrypt_rsa
        symmetric_key = decrypt_rsa(private_key, encrypted_sym_key)
        
        self.log.emit(f"[INFO] Чтение исходного файла: {self.kwargs['input_file']}")
        data = read_bytes(self.kwargs['input_file'])
        
        self.log.emit(f"[INFO] Шифрование данных алгоритмом Blowfish (CBC режим)")
        from crypto_symmetric import encrypt_blowfish
        encrypted_data = encrypt_blowfish(symmetric_key, data)
        
        write_bytes(self.kwargs['output_file'], encrypted_data)
        self.log.emit(f"[OK] Файл успешно зашифрован: {self.kwargs['output_file']}")
        self.finished.emit(True, "Файл успешно зашифрован!")

    def _decrypt_file(self):
        """
        Расшифровывает файл с использованием гибридной схемы.
        """
        self.log.emit(f"[INFO] Чтение зашифрованного симметричного ключа")
        encrypted_sym_key = read_bytes(self.kwargs['encrypted_sym_path'])
        
        self.log.emit(f"[INFO] Загрузка приватного ключа RSA")
        from crypto_asymmetric import load_private_key
        private_key = load_private_key(self.kwargs['private_key_path'])
        
        self.log.emit(f"[INFO] Расшифровка симметричного ключа через RSA")
        from crypto_asymmetric import decrypt_rsa
        symmetric_key = decrypt_rsa(private_key, encrypted_sym_key)
        
        self.log.emit(f"[INFO] Чтение зашифрованного файла: {self.kwargs['input_file']}")
        encrypted_data = read_bytes(self.kwargs['input_file'])
        
        self.log.emit(f"[INFO] Дешифрование данных алгоритмом Blowfish (CBC режим)")
        from crypto_symmetric import decrypt_blowfish
        decrypted_data = decrypt_blowfish(symmetric_key, encrypted_data)
        
        write_bytes(self.kwargs['output_file'], decrypted_data)
        self.log.emit(f"[OK] Файл успешно расшифрован: {self.kwargs['output_file']}")
        self.finished.emit(True, "Файл успешно расшифрован!")


class HybridCryptoApp(QMainWindow):
    """
    Главное окно приложения гибридной криптосистемы RSA + Blowfish.
    """
    
    def __init__(self):
        super().__init__()
        self.settings_file = "app_settings.json"
        self.settings = load_settings(self.settings_file)
        self.worker = None
        self.init_ui()
        self.load_saved_paths()
        self.apply_style()

    def apply_style(self):
        """
        Применяет CSS стили для оформления интерфейса.
        """
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
        """
        Инициализирует пользовательский интерфейс.
        """
        self.setWindowTitle("Гибридная криптосистема RSA + Blowfish")
        self.setGeometry(100, 100, 1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        self._create_header(layout)
        self._create_tabs(layout)
        self._create_status_bar()

    def _create_header(self, layout):
        """
        Создаёт верхнюю панель с заголовком приложения.
        
        Args:
            layout: Родительский компоновщик
        """
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
        
        subtitle = QLabel("RSA (2048 бит) + Blowfish (32-448 бит, режим CBC)")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #1e1e2e; font-size: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)

    def _create_tabs(self, layout):
        """
        Создаёт вкладки приложения.
        
        Args:
            layout: Родительский компоновщик
        """
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.setup_generation_tab()
        self.setup_encryption_tab()
        self.setup_decryption_tab()
        self.setup_log_tab()

    def _create_status_bar(self):
        """
        Создаёт строку состояния с индикатором прогресса.
        """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress)

    def setup_generation_tab(self):
        """
        Настраивает вкладку генерации ключей.
        """
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

        grid.addWidget(QLabel("Длина ключа Blowfish (32-448, кратно 8):"), 3, 0)
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
        """
        Настраивает вкладку шифрования файлов.
        """
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
        """
        Настраивает вкладку дешифрования файлов.
        """
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
        """
        Настраивает вкладку с логами операций.
        """
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
        """
        Открывает диалог выбора или сохранения файла.
        
        Args:
            line_edit: Поле для ввода пути
            save (bool): Если True - диалог сохранения, иначе - открытия
        """
        if save:
            path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Все файлы (*.*)")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Все файлы (*.*)")
        if path:
            line_edit.setText(path)
            self.save_current_paths()

    def save_current_paths(self):
        """
        Сохраняет текущие пути из полей ввода в файл настроек.
        """
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
        """
        Загружает сохранённые пути из файла настроек в поля ввода.
        """
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
        """
        Добавляет сообщение в лог с временной меткой.
        
        Args:
            message (str): Сообщение для добавления
        """
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.appendPlainText(f"[{timestamp}] {message}")

    def set_buttons_enabled(self, enabled):
        """
        Включает или отключает кнопки управления.
        
        Args:
            enabled (bool): True - кнопки активны, False - заблокированы
        """
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
        """
        Обрабатывает завершение операции в рабочем потоке.
        
        Args:
            success (bool): Успешность выполнения операции
            message (str): Сообщение о результате
        """
        self.set_buttons_enabled(True)
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.critical(self, "Ошибка", message)

    def generate_keys(self):
        """
        Запускает процесс генерации ключей.
        """
        if not self.pub_key.text() or not self.priv_key.text() or not self.enc_key.text():
            QMessageBox.warning(self, "Ошибка", "Заполните все пути для сохранения ключей")
            return
        
        key_len = self.key_len.value()
        if key_len % 8 != 0:
            QMessageBox.warning(self, "Ошибка", "Длина ключа Blowfish должна быть кратна 8")
            return
        
        self.set_buttons_enabled(False)
        self.worker = WorkerThread(
            operation='generate',
            public_path=self.pub_key.text(),
            secret_path=self.priv_key.text(),
            encrypted_sym_path=self.enc_key.text(),
            key_length=key_len
        )
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def encrypt_file(self):
        """
        Запускает процесс шифрования файла.
        """
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
        """
        Запускает процесс дешифрования файла.
        """
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
    """
    Главная функция запуска приложения.
    """
    app = QApplication(sys.argv)
    window = HybridCryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
