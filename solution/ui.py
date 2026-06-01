import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect

from hmac_logic import create_hmac
from send_and_receive import send_message, receive_message
from load_and_save import read_data  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HMAC Защита сообщений")
        self.setFixedSize(800, 600)

        self.bg_image_path = "ronaldo.jpg"
        self.sound_path = "sui.wav"

        self.sound_effect = QSoundEffect()
        if os.path.exists(self.sound_path):
            self.sound_effect.setSource(QUrl.fromLocalFile(os.path.abspath(self.sound_path)))

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 800, 600)
        self.update_background()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(550, 500)  
        card.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 225);
                border-radius: 12px;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QLineEdit, QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #ccff00;
            }
            QPushButton {
                background-color: #ccff00;
                color: #000000;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b3e600;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 25, 35, 25)
        card_layout.setSpacing(10)

        title_label = QLabel("СИСТЕМА ЦЕЛОСТНОСТИ ДАННЫХ")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #ccff00; background-color: transparent;")
        card_layout.addWidget(title_label)

        card_layout.addWidget(QLabel("Секретный ключ:"))
        
        key_layout = QHBoxLayout()
        self.input_key = QLineEdit()
        self.input_key.setEchoMode(QLineEdit.EchoMode.Password)
        key_layout.addWidget(self.input_key)
        
        self.btn_load_key = QPushButton("Загрузить")
        self.btn_load_key.setFixedWidth(90)
        self.btn_load_key.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                padding: 6px;
                font-size: 10pt;
                font-weight: normal;
            }
            QPushButton:hover { background-color: #444444; }
        """)
        self.btn_load_key.clicked.connect(self.handle_load_key)
        key_layout.addWidget(self.btn_load_key)
        card_layout.addLayout(key_layout)

        data_header_layout = QHBoxLayout()
        data_header_layout.addWidget(QLabel("Данные:"))
        
        self.btn_load_data = QPushButton("Загрузить файл")
        self.btn_load_data.setFixedWidth(130)
        self.btn_load_data.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                padding: 4px;
                font-size: 10pt;
                font-weight: normal;
            }
            QPushButton:hover { background-color: #444444; }
        """)
        self.btn_load_data.clicked.connect(self.handle_load_data)
        data_header_layout.addWidget(self.btn_load_data, alignment=Qt.AlignmentFlag.AlignRight)
        card_layout.addLayout(data_header_layout)

        self.input_data = QTextEdit()
        card_layout.addWidget(self.input_data)

        self.btn_send = QPushButton("Подписать и Отправить (SIUUU!)")
        self.btn_send.clicked.connect(self.handle_send)
        card_layout.addWidget(self.btn_send)

        self.btn_receive = QPushButton("Открыть и Проверить данные")
        self.btn_receive.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.btn_receive.clicked.connect(self.handle_receive)
        card_layout.addWidget(self.btn_receive)

        self.lbl_status = QLabel("Система готова")
        status_font = QFont("Arial", 10)
        status_font.setItalic(True)
        self.lbl_status.setFont(status_font)
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("color: #888; background-color: transparent;")
        card_layout.addWidget(self.lbl_status)

        main_layout.addWidget(card)

    def show_silent_message(self, title, text):
        """Создает всплывающее окно без системного звука Windows и в темном стиле"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.NoIcon) 
        
        msg.setStyleSheet("""
            QMessageBox { background-color: #141414; }
            QLabel { color: white; font-size: 11pt; }
            QPushButton {
                background-color: #ccff00;
                color: black;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px 20px;
                min-width: 70px;
            }
            QPushButton:hover { background-color: #b3e600; }
        """)
        msg.exec()
    
    def update_background(self):
        """Устанавливает фоновое изображение, масштабируя его по размеру окна, или устанавливает темный фон, если изображение не найдено"""
        if os.path.exists(self.bg_image_path):
            pixmap = QPixmap(self.bg_image_path)
            scaled_pixmap = pixmap.scaled(
                self.size(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.bg_label.setPixmap(scaled_pixmap)
            self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.bg_label.setStyleSheet("background-color: #111;")

    def play_action_sound(self):
        """Проигрывает звук действия, если файл звука доступен """ 
        if self.sound_effect.source():
            self.sound_effect.play()

    def handle_load_key(self):
        """Чтение секретного ключа из любого текстового файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл ключа", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            key_content = read_data(file_path).strip()
            if key_content:
                self.input_key.setText(key_content)
                self.lbl_status.setText("Ключ успешно загружен")
                self.lbl_status.setStyleSheet("color: #ccff00; background-color: transparent;")
            else:
                self.show_silent_message("Ошибка", "Файл ключа пуст или не найден.")

    def handle_load_data(self):
        """Чтение сырых данных / сообщения из текстового файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл с данными", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            data_content = read_data(file_path)
            self.input_data.setText(data_content)
            self.lbl_status.setText("Данные загружены из внешнего файла")
            self.lbl_status.setStyleSheet("color: #ccff00; background-color: transparent;")

    def handle_send(self):
        """Генерация HMAC подписи и сохранение данных с подписью в JSON файл"""
        key = self.input_key.text().strip()
        data = self.input_data.toPlainText().strip()

        if not key or not data:
            self.show_silent_message("", "Заполните ключ и сообщение!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить сообщение", "", "JSON Files (*.json)"
        )
        if not file_path:
            return

        try:
            hmac_hash = create_hmac(key, data)
            send_message(data, hmac_hash, file_path)
            
            self.play_action_sound()
            self.lbl_status.setText(f"Данные успешно сохранены")
            self.lbl_status.setStyleSheet("color: #ccff00; background-color: transparent;")
            self.show_silent_message("УрА!", "Данные защищены и сохранены!\n\nSIUUU!")
        except Exception as e:
            self.lbl_status.setText("Ошибка при сохранении")
            self.lbl_status.setStyleSheet("color: #ff3333; background-color: transparent;")
            self.show_silent_message("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def handle_receive(self):
        """Чтение данных и HMAC из JSON файла, проверка целостности и отображение результата"""
        key = self.input_key.text().strip()

        if not key:
            self.show_silent_message("", "Введите ключ для проверки!")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть сообщение", "", "JSON Files (*.json)"
        )
        if not file_path:
            return

        is_valid, content = receive_message(key, file_path)
        
        self.play_action_sound()

        if is_valid:
            self.input_data.setText(content)
            self.lbl_status.setText("Данные подлинны (HMAC совпал)")
            self.lbl_status.setStyleSheet("color: #ccff00; background-color: transparent;")
            self.show_silent_message("", "Проверка пройдена. Целостность подтверждена!")
        else:
            self.input_data.setText(content)
            self.lbl_status.setText("ДАННЫЕ ПОВРЕЖДЕНЫ: HMAC не совпадает!")
            self.lbl_status.setStyleSheet("color: #ff3333; background-color: transparent;")
            self.show_silent_message("", "Ошибка целостности!\nКлюч неверен или файл был изменен.")