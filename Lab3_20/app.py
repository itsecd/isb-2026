# app.py
import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                             QSlider, QFrame, QGroupBox, QTextEdit, QMessageBox,
                             QProgressBar, QComboBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QTabWidget, QGridLayout, QSplitter)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QLinearGradient, QBrush
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os as os_module


class CryptoWorker(QThread):
    """Поток для выполнения криптографических операций"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, settings, key_size=None):
        super().__init__()
        self.operation = operation  # 'generation', 'encryption', 'decryption'
        self.settings = settings
        self.key_size = key_size
        
    def run(self):
        try:
            if self.operation == 'generation':
                self.generate_keys()
            elif self.operation == 'encryption':
                self.encrypt_file()
            elif self.operation == 'decryption':
                self.decrypt_file()
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def generate_camellia_key(self, key_size_bits):
        return os_module.urandom(key_size_bits // 8)
    
    def generate_rsa_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        return private_key, private_key.public_key()
    
    def save_rsa_keys(self, private_key, public_key, private_path, public_path):
        os_module.makedirs(os_module.path.dirname(private_path), exist_ok=True)
        os_module.makedirs(os_module.path.dirname(public_path), exist_ok=True)
        
        with open(private_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(public_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def encrypt_symmetric_key(self, sym_key, public_key, output_path):
        encrypted_key = public_key.encrypt(
            sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        with open(output_path, 'wb') as f:
            f.write(encrypted_key)
    
    def decrypt_symmetric_key(self, private_key, encrypted_key_path):
        with open(encrypted_key_path, 'rb') as f:
            encrypted_key = f.read()
        
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def encrypt_file_content(self, input_path, output_path, key):
        with open(input_path, 'rb') as f:
            data = f.read()
        
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        iv = os_module.urandom(16)
        
        cipher = Cipher(
            algorithms.Camellia(key),
            modes.CBC(iv)
        )
        
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
    
    def decrypt_file_content(self, input_path, output_path, key):
        with open(input_path, 'rb') as f:
            file_data = f.read()
        
        iv = file_data[:16]
        ciphertext = file_data[16:]
        
        cipher = Cipher(
            algorithms.Camellia(key),
            modes.CBC(iv)
        )
        
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = sym_padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        with open(output_path, 'wb') as f:
            f.write(data)
    
    def generate_keys(self):
        self.status.emit("Генерация симметричного ключа Camellia...")
        self.progress.emit(20)
        sym_key = self.generate_camellia_key(self.key_size)
        
        self.status.emit("Генерация RSA ключей...")
        self.progress.emit(40)
        private_key, public_key = self.generate_rsa_keys()
        
        self.status.emit("Сохранение RSA ключей...")
        self.progress.emit(60)
        self.save_rsa_keys(
            private_key,
            public_key,
            self.settings["private_key"],
            self.settings["public_key"]
        )
        
        self.status.emit("Шифрование симметричного ключа...")
        self.progress.emit(80)
        self.encrypt_symmetric_key(
            sym_key,
            public_key,
            self.settings["symmetric_key_encrypted"]
        )
        
        self.progress.emit(100)
        self.status.emit("Генерация ключей завершена!")
        self.finished.emit(True, "Ключи успешно сгенерированы!")
    
    def encrypt_file(self):
        self.status.emit("Загрузка приватного ключа...")
        self.progress.emit(10)
        
        with open(self.settings["private_key"], 'rb') as f:
            private_key_data = f.read()
        private_key = serialization.load_pem_private_key(private_key_data, password=None)
        
        self.status.emit("Расшифровка симметричного ключа...")
        self.progress.emit(30)
        sym_key = self.decrypt_symmetric_key(private_key, self.settings["symmetric_key_encrypted"])
        
        self.status.emit("Шифрование файла...")
        self.progress.emit(60)
        self.encrypt_file_content(
            self.settings["initial_file"],
            self.settings["encrypted_file"],
            sym_key
        )
        
        self.progress.emit(100)
        self.status.emit("Шифрование завершено!")
        self.finished.emit(True, "Файл успешно зашифрован!")
    
    def decrypt_file(self):
        self.status.emit("Загрузка приватного ключа...")
        self.progress.emit(10)
        
        with open(self.settings["private_key"], 'rb') as f:
            private_key_data = f.read()
        private_key = serialization.load_pem_private_key(private_key_data, password=None)
        
        self.status.emit("Расшифровка симметричного ключа...")
        self.progress.emit(30)
        sym_key = self.decrypt_symmetric_key(private_key, self.settings["symmetric_key_encrypted"])
        
        self.status.emit("Дешифрование файла...")
        self.progress.emit(60)
        self.decrypt_file_content(
            self.settings["encrypted_file"],
            self.settings["decrypted_file"],
            sym_key
        )
        
        self.progress.emit(100)
        self.status.emit("Дешифрование завершено!")
        self.finished.emit(True, "Файл успешно дешифрован!")


class CryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.worker = None
        self.initUI()
        
    def load_settings(self):
        """Загрузка настроек из файла"""
        settings_path = "settings.json"
        default_settings = {
            "initial_file": "data/input.txt",
            "encrypted_file": "data/encrypted.bin",
            "decrypted_file": "data/decrypted.txt",
            "symmetric_key_encrypted": "keys/symmetric.key.enc",
            "public_key": "keys/public.pem",
            "private_key": "keys/private.pem"
        }
        
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                for key in default_settings:
                    if key not in settings:
                        settings[key] = default_settings[key]
                return settings
            except:
                return default_settings
        return default_settings
    
    def initUI(self):
        self.setWindowTitle('Hybrid Crypto System - Лабораторная работа')
        self.setGeometry(100, 100, 1000, 750)
        
        # Установка фиолетовой цветовой схемы
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a0b2e, stop:1 #2d1b4e);
            }
            QLabel {
                color: #e0d4f7;
                font-size: 12px;
            }
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
            QPushButton:pressed {
                background-color: #4a235a;
            }
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
                min-width: 80px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #c39bd3;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2c1838;
                color: #e0d4f7;
                selection-background-color: #6c3483;
                border: 1px solid #6c3483;
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
            QTabBar::tab:hover {
                background-color: #512e6b;
            }
            QScrollBar:vertical {
                background-color: #1a0f2a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #6c3483;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
            }
            QMessageBox {
                background-color: #2d1b4e;
                color: #e0d4f7;
            }
            QMessageBox QPushButton {
                min-width: 80px;
            }
        """)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        
        # Заголовок с градиентом
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a235a, stop:1 #6c3483);
                border-radius: 10px;
                padding: 5px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("🔐 Гибридная криптосистема (RSA-2048 + Camellia)")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #f0e6ff; padding: 10px;")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Лабораторная работа по криптографии")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #c39bd3; font-size: 11px; padding-bottom: 5px;")
        title_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # Вкладки
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Вкладка управления
        control_tab = QWidget()
        tabs.addTab(control_tab, "🎮 Управление")
        
        # Вкладка информации
        info_tab = QWidget()
        tabs.addTab(info_tab, "ℹ️ Информация")
        
        # Вкладка логов
        logs_tab = QWidget()
        tabs.addTab(logs_tab, "📋 Логи")
        
        # Настройка вкладки управления
        control_layout = QVBoxLayout(control_tab)
        
        # Группа настроек файлов
        files_group = QGroupBox("📁 Настройки файлов")
        files_layout = QGridLayout()
        files_layout.setSpacing(10)
        
        # Пути к файлам
        self.file_paths = {}
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
            btn.clicked.connect(lambda checked, k=key: self.select_file(k))
            
            files_layout.addWidget(label, row, 0)
            files_layout.addWidget(path_label, row, 1)
            files_layout.addWidget(btn, row, 2)
        
        files_group.setLayout(files_layout)
        control_layout.addWidget(files_group)
        
        # Группа операций
        operations_group = QGroupBox("⚡ Криптографические операции")
        operations_layout = QVBoxLayout()
        operations_layout.setSpacing(15)
        
        # Выбор размера ключа
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("🎯 Размер ключа Camellia:"))
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["128", "192", "256"])
        self.key_size_combo.setFixedWidth(80)
        key_layout.addWidget(self.key_size_combo)
        key_layout.addStretch()
        operations_layout.addLayout(key_layout)
        
        # Кнопки операций
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        self.gen_btn = QPushButton("🔑 Генерация ключей")
        self.gen_btn.setMinimumHeight(40)
        self.gen_btn.clicked.connect(self.generate_keys)
        self.gen_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e44ad, stop:1 #6c3483);
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a569bd, stop:1 #7d3c98);
            }
        """)
        buttons_layout.addWidget(self.gen_btn)
        
        self.enc_btn = QPushButton("🔒 Шифрование файла")
        self.enc_btn.setMinimumHeight(40)
        self.enc_btn.clicked.connect(self.encrypt_file)
        self.enc_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
        """)
        buttons_layout.addWidget(self.enc_btn)
        
        self.dec_btn = QPushButton("🔓 Дешифрование файла")
        self.dec_btn.setMinimumHeight(40)
        self.dec_btn.clicked.connect(self.decrypt_file)
        self.dec_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #52be80, stop:1 #2ecc71);
            }
        """)
        buttons_layout.addWidget(self.dec_btn)
        
        operations_layout.addLayout(buttons_layout)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(25)
        operations_layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel("✅ Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            padding: 12px; 
            background-color: #1a0f2a; 
            border-radius: 8px;
            font-weight: bold;
            border: 1px solid #6c3483;
        """)
        operations_layout.addWidget(self.status_label)
        
        operations_group.setLayout(operations_layout)
        control_layout.addWidget(operations_group)
        
        # Краткий лог на главной вкладке
        quick_log_group = QGroupBox("📝 Последние операции")
        quick_log_layout = QVBoxLayout()
        self.quick_log_text = QTextEdit()
        self.quick_log_text.setReadOnly(True)
        self.quick_log_text.setMaximumHeight(150)
        self.quick_log_text.setStyleSheet("font-family: monospace; font-size: 10px;")
        quick_log_layout.addWidget(self.quick_log_text)
        quick_log_group.setLayout(quick_log_layout)
        control_layout.addWidget(quick_log_group)
        
        # Настройка вкладки информации
        info_layout = QVBoxLayout(info_tab)
        
        # Информация о системе
        info_group = QGroupBox("📚 О системе")
        info_text = QLabel("""
        <h2 style="color: #c39bd3;">Гибридная криптосистема</h2>
        
        <h3 style="color: #d4b8ff;">🔐 Используемые алгоритмы:</h3>
        <ul>
            <li><b>Асимметричное шифрование:</b> RSA-2048 (OAEP с SHA-256)</li>
            <li><b>Симметричное шифрование:</b> Camellia-CBC (128/192/256 бит)</li>
            <li><b>Режим:</b> CBC с PKCS7 паддингом</li>
        </ul>
        
        <h3 style="color: #d4b8ff;">⚙️ Принцип работы:</h3>
        <ol>
            <li>Генерируется случайный симметричный ключ Camellia</li>
            <li>Генерируется пара RSA ключей (2048 бит)</li>
            <li>Симметричный ключ шифруется публичным RSA ключом</li>
            <li>Файл шифруется симметричным ключом Camellia</li>
        </ol>
        
        <h3 style="color: #d4b8ff;">✨ Преимущества:</h3>
        <ul>
            <li>Высокая скорость обработки больших файлов (за счет симметричного шифрования)</li>
            <li>Безопасная передача ключа (за счет асимметричного шифрования)</li>
            <li>Поддержка ключей различной длины</li>
            <li>Криптостойкость на уровне AES</li>
        </ul>
        
        <h3 style="color: #d4b8ff;">📂 Структура папок:</h3>
        <ul>
            <li><b>data/</b> - исходные, зашифрованные и расшифрованные файлы</li>
            <li><b>keys/</b> - RSA ключи и зашифрованный симметричный ключ</li>
        </ul>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 15px; line-height: 1.5;")
        info_layout.addWidget(info_text)
        
        # Таблица с информацией о файлах
        files_info_group = QGroupBox("📊 Информация о файлах")
        files_info_layout = QVBoxLayout()
        
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Тип файла", "Путь", "Размер", "Статус"])
        self.files_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.files_table.setAlternatingRowColors(True)
        self.files_table.setStyleSheet("alternate-background-color: #2a1540;")
        
        files_info_layout.addWidget(self.files_table)
        files_info_group.setLayout(files_info_layout)
        info_layout.addWidget(files_info_group)
        
        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить информацию о файлах")
        refresh_btn.setFixedHeight(35)
        refresh_btn.clicked.connect(self.update_files_info)
        info_layout.addWidget(refresh_btn)
        
        # Настройка вкладки логов
        logs_layout = QVBoxLayout(logs_tab)
        
        logs_group = QGroupBox("📜 Полный лог операций")
        logs_layout_inner = QVBoxLayout()
        self.full_log_text = QTextEdit()
        self.full_log_text.setReadOnly(True)
        self.full_log_text.setStyleSheet("font-family: monospace; font-size: 11px;")
        logs_layout_inner.addWidget(self.full_log_text)
        
        # Кнопки управления логом
        log_buttons_layout = QHBoxLayout()
        clear_log_btn = QPushButton("🗑️ Очистить лог")
        clear_log_btn.clicked.connect(self.clear_logs)
        log_buttons_layout.addWidget(clear_log_btn)
        log_buttons_layout.addStretch()
        logs_layout_inner.addLayout(log_buttons_layout)
        
        logs_group.setLayout(logs_layout_inner)
        logs_layout.addWidget(logs_group)
        
        # Добавляем информацию о файлах
        self.update_files_info()
        
        # Лог первого сообщения
        self.log_message("🚀 Приложение запущено")
        self.log_message("📁 Используются папки: data/ и keys/")
        
    def select_file(self, key):
        """Выбор файла"""
        if key in ["public_key", "private_key"]:
            file_filter = "PEM files (*.pem);;All files (*.*)"
        elif key == "symmetric_key_encrypted":
            file_filter = "Encrypted files (*.enc);;All files (*.*)"
        elif key in ["encrypted_file"]:
            file_filter = "Binary files (*.bin);;All files (*.*)"
        else:
            file_filter = "Text files (*.txt);;All files (*.*)"
        
        # Устанавливаем начальную директорию
        if "data" in self.settings.get(key, ""):
            initial_dir = "data"
        elif "keys" in self.settings.get(key, ""):
            initial_dir = "keys"
        else:
            initial_dir = ""
        
        file_path, _ = QFileDialog.getOpenFileName(self, f"Выберите файл", initial_dir, file_filter)
        if file_path:
            self.settings[key] = file_path
            self.file_paths[key].setText(file_path)
            self.log_message(f"📂 Выбран файл: {file_path}")
            self.update_files_info()
    
    def log_message(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.quick_log_text.append(log_entry)
        self.full_log_text.append(log_entry)
        
        # Автопрокрутка вниз
        scrollbar = self.quick_log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        scrollbar = self.full_log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_logs(self):
        """Очистка логов"""
        self.quick_log_text.clear()
        self.full_log_text.clear()
        self.log_message("🧹 Лог очищен")
    
    def update_files_info(self):
        """Обновление информации о файлах в таблице"""
        self.files_table.setRowCount(0)
        row = 0
        
        file_list = [
            ("📄 Исходный файл", "initial_file", "data/input.txt"),
            ("🔒 Зашифрованный файл", "encrypted_file", "data/encrypted.bin"),
            ("🔓 Расшифрованный файл", "decrypted_file", "data/decrypted.txt"),
            ("🔑 Публичный ключ", "public_key", "keys/public.pem"),
            ("🗝️ Приватный ключ", "private_key", "keys/private.pem"),
            ("🔐 Зашифрованный ключ", "symmetric_key_encrypted", "keys/symmetric.key.enc")
        ]
        
        for display_name, key, default_path in file_list:
            if key not in self.settings:
                self.settings[key] = default_path
            
            file_path = self.settings.get(key, "")
            self.files_table.insertRow(row)
            
            # Тип файла
            type_item = QTableWidgetItem(display_name)
            type_item.setForeground(QColor(196, 155, 211))
            type_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.files_table.setItem(row, 0, type_item)
            
            # Путь
            path_item = QTableWidgetItem(file_path if file_path else "Не указан")
            path_item.setForeground(QColor(224, 212, 247))
            self.files_table.setItem(row, 1, path_item)
            
            # Размер
            if file_path and os.path.exists(file_path):
                size = os.path.getsize(file_path)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.2f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.2f} MB"
                size_item = QTableWidgetItem(size_str)
                size_item.setForeground(QColor(144, 238, 144))
            else:
                size_item = QTableWidgetItem("❌ Не найден")
                size_item.setForeground(QColor(255, 160, 122))
            self.files_table.setItem(row, 2, size_item)
            
            # Статус
            if file_path and os.path.exists(file_path):
                status_item = QTableWidgetItem("✓ Доступен")
                status_item.setForeground(QColor(144, 238, 144))
            else:
                status_item = QTableWidgetItem("✗ Отсутствует")
                status_item.setForeground(QColor(255, 160, 122))
            self.files_table.setItem(row, 3, status_item)
            
            row += 1
        
        self.files_table.resizeColumnsToContents()
    
    def set_buttons_enabled(self, enabled):
        """Включение/выключение кнопок"""
        self.gen_btn.setEnabled(enabled)
        self.enc_btn.setEnabled(enabled)
        self.dec_btn.setEnabled(enabled)
        self.key_size_combo.setEnabled(enabled)
    
    def generate_keys(self):
        """Генерация ключей"""
        key_size = int(self.key_size_combo.currentText())
        
        self.set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('generation', self.settings, key_size)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()
        
        self.log_message(f"🔑 Начало генерации ключей (размер Camellia: {key_size} бит)")
    
    def encrypt_file(self):
        """Шифрование файла"""
        # Проверка наличия файлов
        if not os.path.exists(self.settings["initial_file"]):
            QMessageBox.warning(self, "Ошибка", "❌ Исходный файл не найден!\n\nУбедитесь, что файл существует в папке data/")
            return
        
        if not os.path.exists(self.settings["private_key"]):
            QMessageBox.warning(self, "Ошибка", "❌ Приватный ключ не найден!\n\nСначала сгенерируйте ключи (кнопка 'Генерация ключей')")
            return
        
        if not os.path.exists(self.settings["symmetric_key_encrypted"]):
            QMessageBox.warning(self, "Ошибка", "❌ Зашифрованный симметричный ключ не найден!\n\nСначала сгенерируйте ключи (кнопка 'Генерация ключей')")
            return
        
        self.set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('encryption', self.settings)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()
        
        self.log_message(f"🔒 Начало шифрования файла: {self.settings['initial_file']}")
    
    def decrypt_file(self):
        """Дешифрование файла"""
        if not os.path.exists(self.settings["encrypted_file"]):
            QMessageBox.warning(self, "Ошибка", "❌ Зашифрованный файл не найден!\n\nСначала зашифруйте файл или проверьте наличие файла в папке data/")
            return
        
        if not os.path.exists(self.settings["private_key"]):
            QMessageBox.warning(self, "Ошибка", "❌ Приватный ключ не найден!\n\nНевозможно дешифровать без приватного ключа")
            return
        
        self.set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = CryptoWorker('decryption', self.settings)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.start()
        
        self.log_message(f"🔓 Начало дешифрования файла: {self.settings['encrypted_file']}")
    
    def on_operation_finished(self, success, message):
        """Обработка завершения операции"""
        self.set_buttons_enabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self.log_message(f"✅ {message}")
            self.status_label.setText(f"✅ {message}")
            self.status_label.setStyleSheet("""
                padding: 12px; 
                background-color: #1a0f2a; 
                border-radius: 8px;
                font-weight: bold;
                border: 1px solid #27ae60;
                color: #2ecc71;
            """)
            QMessageBox.information(self, "Успех", f"✅ {message}\n\nРезультат сохранен в соответствующий файл.")
            self.update_files_info()
        else:
            self.log_message(f"❌ Ошибка: {message}")
            self.status_label.setText(f"❌ Ошибка: {message}")
            self.status_label.setStyleSheet("""
                padding: 12px; 
                background-color: #1a0f2a; 
                border-radius: 8px;
                font-weight: bold;
                border: 1px solid #c0392b;
                color: #e74c3c;
            """)
            QMessageBox.critical(self, "Ошибка", f"❌ {message}")
        
        # Сброс стиля через 3 секунды
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet("""
            padding: 12px; 
            background-color: #1a0f2a; 
            border-radius: 8px;
            font-weight: bold;
            border: 1px solid #6c3483;
        """))
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Сохраняем настройки
        with open("settings.json", 'w') as f:
            json.dump(self.settings, f, indent=4)
        self.log_message("👋 Приложение закрыто")
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Установка иконки приложения
    app.setApplicationName("Hybrid Crypto System")
    
    window = CryptoApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()