# app.py
"""GUI интерфейс для гибридной криптосистемы"""

import sys
import os
from datetime import datetime
from typing import Dict, Any

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QFileDialog, QFrame, QGroupBox, QTextEdit, QMessageBox,
    QProgressBar, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QTabWidget, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from file_utils import load_json_settings, save_json_settings, get_file_size_str
from hybrid_crypto import generate_hybrid_keys, encrypt_hybrid, decrypt_hybrid


class CryptoWorker(QThread):
    """Поток для выполнения криптографических операций"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation: str, settings: Dict[str, Any], key_size: int = None):
        super().__init__()
        self.operation = operation
        self.settings = settings
        self.key_size = key_size
        
    def run(self):
        try:
            match self.operation:
                case 'generation':
                    self._generate()
                case 'encryption':
                    self._encrypt()
                case 'decryption':
                    self._decrypt()
                case _:
                    self.finished.emit(False, f"Неизвестная операция: {self.operation}")
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def _generate(self):
        self.status.emit("Генерация ключей...")
        self.progress.emit(50)
        success, message = generate_hybrid_keys(self.settings, self.key_size)
        self.progress.emit(100)
        self.finished.emit(success, message)
    
    def _encrypt(self):
        self.status.emit("Подготовка к шифрованию...")
        self.progress.emit(20)
        success, message = encrypt_hybrid(self.settings)
        self.progress.emit(100)
        self.finished.emit(success, message)
    
    def _decrypt(self):
        self.status.emit("Подготовка к расшифрованию...")
        self.progress.emit(20)
        success, message = decrypt_hybrid(self.settings)
        self.progress.emit(100)
        self.finished.emit(success, message)


class CryptoApp(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.settings_file = "settings.json"
        self.settings = self._load_settings()
        self.worker = None
        self.file_paths = {}
        self._init_ui()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Загрузка настроек"""
        default_settings = {
            "initial_file": "data/input.txt",
            "encrypted_file": "data/encrypted.bin",
            "decrypted_file": "data/decrypted.txt",
            "symmetric_key_encrypted": "keys/symmetric.key.enc",
            "public_key": "keys/public.pem",
            "private_key": "keys/private.pem"
        }
        
        try:
            return load_json_settings(self.settings_file, default_settings)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            return default_settings
    
    def _save_settings(self):
        """Сохранение настроек"""
        try:
            save_json_settings(self.settings_file, self.settings)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def _init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('🔐 Гибридная криптосистема (RSA-2048 + Camellia)')
        self.setGeometry(100, 100, 1000, 750)
        
        self._apply_styles()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        
        main_layout.addWidget(self._create_header())
        
        tabs = QTabWidget()
        tabs.addTab(self._create_control_tab(), "🎮 Управление")
        tabs.addTab(self._create_info_tab(), "ℹ️ Информация")
        tabs.addTab(self._create_logs_tab(), "📋 Логи")
        main_layout.addWidget(tabs)
        
        self._update_files_info()
        self._log_message("🚀 Приложение запущено")
    
    def _apply_styles(self):
        """Применение CSS стилей"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a0b2e, stop:1 #2d1b4e);
            }
            QLabel { color: #e0d4f7; font-size: 12px; }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c3483, stop:1 #512e6b);
                color: #f0e6ff;
                border: 1px solid #8e44ad;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7d3c98, stop:1 #633974);
                border: 1px solid #a569bd;
            }
            QPushButton:pressed { background-color: #4a235a; }
            QPushButton:disabled {
                background-color: #4a3a5a;
                color: #8a7a9a;
                border: 1px solid #6a5a7a;
            }
            QGroupBox {
                color: #d4b8ff;
                border: 2px solid #6c3483;
                border-radius: 10px;
                margin-top: 12px;
                font-size: 13px;
                font-weight: bold;
                background-color: rgba(44, 24, 64, 0.7);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #c39bd3;
            }
            QTextEdit {
                background-color: #1a0f2a;
                color: #e0d4f7;
                border: 1px solid #6c3483;
                border-radius: 6px;
                font-family: monospace;
            }
            QComboBox {
                background-color: #2c1838;
                color: #e0d4f7;
                border: 1px solid #6c3483;
                border-radius: 5px;
                padding: 5px;
            }
            QProgressBar {
                border: 1px solid #6c3483;
                border-radius: 5px;
                text-align: center;
                color: #f0e6ff;
                background-color: #1a0f2a;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8e44ad, stop:1 #c39bd3);
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #1a0f2a;
                color: #e0d4f7;
                border: 1px solid #6c3483;
                border-radius: 6px;
                gridline-color: #4a2a6a;
            }
            QHeaderView::section {
                background-color: #2c1838;
                color: #d4b8ff;
                padding: 6px;
                border: 1px solid #6c3483;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid #6c3483;
                border-radius: 8px;
                background-color: rgba(44, 24, 64, 0.5);
            }
            QTabBar::tab {
                background-color: #2c1838;
                color: #d4b8ff;
                padding: 8px 20px;
                margin-right: 3px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #6c3483;
                color: #f0e6ff;
            }
            QTabBar::tab:hover { background-color: #512e6b; }
        """)
    
    def _create_header(self) -> QFrame:
        """Создание заголовка приложения"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a235a, stop:1 #6c3483);
                border-radius: 10px;
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout(header)
        
        title = QLabel("🔐 Гибридная криптосистема (RSA-2048 + Camellia)")
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #f0e6ff; padding: 10px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Лабораторная работа по криптографии")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #c39bd3; font-size: 11px; padding-bottom: 5px;")
        layout.addWidget(subtitle)
        
        return header
    
    def _create_control_tab(self) -> QWidget:
        """Создание вкладки управления"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        layout.addWidget(self._create_files_group())
        layout.addWidget(self._create_operations_group())
        layout.addWidget(self._create_quick_log_group())
        
        return tab
    
    def _create_files_group(self) -> QGroupBox:
        """Создание группы выбора файлов"""
        group = QGroupBox("📁 Настройки файлов")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        file_configs = [
            ("initial_file", "📄 Исходный файл:", "data/input.txt"),
            ("encrypted_file", "🔒 Зашифрованный файл:", "data/encrypted.bin"),
            ("decrypted_file", "🔓 Расшифрованный файл:", "data/decrypted.txt"),
            ("public_key", "🔑 Публичный ключ:", "keys/public.pem"),
            ("private_key", "🗝️ Приватный ключ:", "keys/private.pem"),
            ("symmetric_key_encrypted", "🔐 Зашифр. симметр. ключ:", "keys/symmetric.key.enc")
        ]
        
        for row, (key, label_text, default_path) in enumerate(file_configs):
            if key not in self.settings:
                self.settings[key] = default_path
            
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            
            path_label = QLabel(self.settings.get(key, ""))
            path_label.setWordWrap(True)
            path_label.setStyleSheet("""
                background-color: #1a0f2a; 
                padding: 6px; 
                border-radius: 5px;
                font-family: monospace;
                font-size: 10px;
            """)
            self.file_paths[key] = path_label
            
            btn = QPushButton("📂 Выбрать")
            btn.setFixedWidth(100)
            btn.clicked.connect(lambda checked, k=key: self._select_file(k))
            
            layout.addWidget(label, row, 0)
            layout.addWidget(path_label, row, 1)
            layout.addWidget(btn, row, 2)
        
        group.setLayout(layout)
        return group
    
    def _create_operations_group(self) -> QGroupBox:
        """Создание группы операций"""
        group = QGroupBox("⚡ Криптографические операции")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🎯 Размер ключа Camellia:"))
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["128", "192", "256"])
        self.key_size_combo.setFixedWidth(80)
        key_layout.addWidget(self.key_size_combo)
        key_layout.addStretch()
        layout.addLayout(key_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        self.gen_btn = QPushButton("🔑 Генерация ключей")
        self.gen_btn.setMinimumHeight(40)
        self.gen_btn.clicked.connect(self._generate_keys)
        buttons_layout.addWidget(self.gen_btn)
        
        self.enc_btn = QPushButton("🔒 Шифрование файла")
        self.enc_btn.setMinimumHeight(40)
        self.enc_btn.clicked.connect(self._encrypt_file)
        buttons_layout.addWidget(self.enc_btn)
        
        self.dec_btn = QPushButton("🔓 Дешифрование файла")
        self.dec_btn.setMinimumHeight(40)
        self.dec_btn.clicked.connect(self._decrypt_file)
        buttons_layout.addWidget(self.dec_btn)
        
        layout.addLayout(buttons_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(25)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("✅ Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            padding: 12px; 
            background-color: #1a0f2a; 
            border-radius: 8px;
            font-weight: bold;
            border: 1px solid #6c3483;
        """)
        layout.addWidget(self.status_label)
        
        group.setLayout(layout)
        return group
    
    def _create_quick_log_group(self) -> QGroupBox:
        """Создание группы быстрого лога"""
        group = QGroupBox("📝 Последние операции")
        layout = QVBoxLayout()
        self.quick_log_text = QTextEdit()
        self.quick_log_text.setReadOnly(True)
        self.quick_log_text.setMaximumHeight(150)
        layout.addWidget(self.quick_log_text)
        group.setLayout(layout)
        return group
    
    def _create_info_tab(self) -> QWidget:
        """Создание вкладки информации"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_text = QLabel("""
        <h2 style="color: #c39bd3;">Гибридная криптосистема</h2>
        <h3>🔐 Используемые алгоритмы:</h3>
        <ul>
            <li><b>RSA-2048</b> (OAEP с SHA-256)</li>
            <li><b>Camellia-CBC</b> (128/192/256 бит)</li>
        </ul>
        <h3>⚙️ Принцип работы:</h3>
        <ol>
            <li>Генерация симметричного ключа Camellia</li>
            <li>Генерация пары RSA ключей</li>
            <li>Шифрование симметричного ключа публичным RSA ключом</li>
            <li>Шифрование файла симметричным ключом (Camellia-CBC)</li>
        </ol>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 15px; line-height: 1.5;")
        layout.addWidget(info_text)
        
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Тип файла", "Путь", "Размер", "Статус"])
        self.files_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.files_table)
        
        refresh_btn = QPushButton("🔄 Обновить информацию")
        refresh_btn.clicked.connect(self._update_files_info)
        layout.addWidget(refresh_btn)
        
        return tab
    
    def _create_logs_tab(self) -> QWidget:
        """Создание вкладки полных логов"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.full_log_text = QTextEdit()
        self.full_log_text.setReadOnly(True)
        layout.addWidget(self.full_log_text)
        
        clear_btn = QPushButton("🗑️ Очистить лог")
        clear_btn.clicked.connect(self._clear_logs)
        layout.addWidget(clear_btn)
        
        return tab
    
    def _select_file(self, key: str):
        """Выбор файла через диалог"""
        filters = {
            "public_key": "PEM files (*.pem)",
            "private_key": "PEM files (*.pem)",
            "symmetric_key_encrypted": "Encrypted files (*.enc)",
            "encrypted_file": "Binary files (*.bin *.enc)",
            "decrypted_file": "Text files (*.txt)",
            "initial_file": "All files (*.*)"
        }
        
        file_filter = filters.get(key, "All files (*.*)")
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        
        if file_path:
            self.settings[key] = file_path
            self.file_paths[key].setText(file_path)
            self._log_message(f"📂 Выбран файл: {file_path}")
            self._update_files_info()
            self._save_settings()
    
    def _log_message(self, message: str):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.quick_log_text.append(log_entry)
        self.full_log_text.append(log_entry)
    
    def _clear_logs(self):
        """Очистка логов"""
        self.quick_log_text.clear()
        self.full_log_text.clear()
        self._log_message("🧹 Лог очищен")
    
    def _update_files_info(self):
        """Обновление информации о файлах"""
        self.files_table.setRowCount(0)
        
        file_list = [
            ("Исходный файл", "initial_file"),
            ("Зашифрованный файл", "encrypted_file"),
            ("Расшифрованный файл", "decrypted_file"),
            ("Публичный ключ", "public_key"),
            ("Приватный ключ", "private_key"),
            ("Зашифр. симметр. ключ", "symmetric_key_encrypted")
        ]
        
        for row, (name, key) in enumerate(file_list):
            path = self.settings.get(key, "")
            self.files_table.insertRow(row)
            self.files_table.setItem(row, 0, QTableWidgetItem(name))
            self.files_table.setItem(row, 1, QTableWidgetItem(path if path else "Не указан"))
            
            if path and os.path.exists(path):
                size_str = get_file_size_str(path)
                self.files_table.setItem(row, 2, QTableWidgetItem(size_str))
                self.files_table.setItem(row, 3, QTableWidgetItem("✓ Доступен"))
            else:
                self.files_table.setItem(row, 2, QTableWidgetItem("-"))
                self.files_table.setItem(row, 3, QTableWidgetItem("✗ Отсутствует"))
        
        self.files_table.resizeColumnsToContents()
    
    def _set_buttons_enabled(self, enabled: bool):
        """Включение/выключение кнопок"""
        self.gen_btn.setEnabled(enabled)
        self.enc_btn.setEnabled(enabled)
        self.dec_btn.setEnabled(enabled)
        self.key_size_combo.setEnabled(enabled)
    
    def _generate_keys(self):
        """Генерация ключей"""
        key_size_bits = int(self.key_size_combo.currentText())
        
        match key_size_bits:
            case 128 | 192 | 256:
                pass
            case _:
                QMessageBox.warning(self, "Ошибка", f"Недопустимый размер ключа: {key_size_bits} бит")
                return
        
        self._set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('generation', self.settings, key_size_bits)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self._on_operation_finished)
        self.worker.start()
        
        self._log_message(f"🔑 Генерация ключей (Camellia-{key_size_bits} бит)")
    
    def _encrypt_file(self):
        """Шифрование файла"""
        match os.path.exists(self.settings.get("initial_file", "")):
            case False:
                QMessageBox.warning(self, "Ошибка", "Исходный файл не найден!")
                return
            case _:
                pass
        
        match os.path.exists(self.settings.get("private_key", "")):
            case False:
                QMessageBox.warning(self, "Ошибка", 
                    "Приватный ключ не найден! Сначала сгенерируйте ключи.")
                return
            case _:
                pass
        
        self._set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('encryption', self.settings)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self._on_operation_finished)
        self.worker.start()
        
        self._log_message(f"🔒 Шифрование: {self.settings['initial_file']}")
    
    def _decrypt_file(self):
        """Расшифрование файла"""
        match os.path.exists(self.settings.get("encrypted_file", "")):
            case False:
                QMessageBox.warning(self, "Ошибка", "Зашифрованный файл не найден!")
                return
            case _:
                pass
        
        self._set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('decryption', self.settings)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self._on_operation_finished)
        self.worker.start()
        
        self._log_message(f"🔓 Дешифрование: {self.settings['encrypted_file']}")
    
    def _on_operation_finished(self, success: bool, message: str):
        """Обработка завершения операции"""
        self._set_buttons_enabled(True)
        self.progress_bar.setVisible(False)
        
        match success:
            case True:
                self._log_message(f" {message}")
                self.status_label.setText(f" {message}")
                QMessageBox.information(self, "Успех", message)
                self._update_files_info()
            case False:
                self._log_message(f" {message}")
                self.status_label.setText(f" {message}")
                QMessageBox.critical(self, "Ошибка", message)
        
        QTimer.singleShot(3000, lambda: self.status_label.setText(" Готов к работе"))
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self._save_settings()
        event.accept()


def main_gui():
    """Запуск GUI приложения"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main_gui()