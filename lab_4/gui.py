import json
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
import create
import packet
import atak
import collision


class HMACApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Интерфейс контроля целостности данных (HMAC)")
        self.setGeometry(100, 100, 750, 550)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Секретный ключ:"))
        self.key_input = QLineEdit()
        key_layout.addWidget(self.key_input)
        main_layout.addLayout(key_layout)

        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Текст сообщения:"))
        self.text_input = QLineEdit()
        text_layout.addWidget(self.text_input)
        self.btn_load_file = QPushButton("Загрузить файл")
        text_layout.addWidget(self.btn_load_file)
        main_layout.addLayout(text_layout)

        sig_layout = QHBoxLayout()
        sig_layout.addWidget(QLabel("HMAC подпись (Hex):"))
        self.sig_input = QLineEdit()
        sig_layout.addWidget(self.sig_input)
        main_layout.addLayout(sig_layout)

        btn_layout = QHBoxLayout()
        self.btn_create = QPushButton("Сформировать HMAC")
        self.btn_verify = QPushButton("Проверить пакет")
        self.btn_attack = QPushButton("Имитировать атаку")
        self.btn_collision = QPushButton("Подобрать коллизию")
        self.btn_save_packet = QPushButton("Сохранить пакет")
        
        btn_layout.addWidget(self.btn_create)
        btn_layout.addWidget(self.btn_verify)
        btn_layout.addWidget(self.btn_attack)
        btn_layout.addWidget(self.btn_collision)
        btn_layout.addWidget(self.btn_save_packet)
        main_layout.addLayout(btn_layout)

        main_layout.addWidget(QLabel("Журнал событий:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.btn_load_file.clicked.connect(self.on_load_file)
        self.btn_save_packet.clicked.connect(self.on_save_packet)
        self.btn_create.clicked.connect(self.on_create)
        self.btn_verify.clicked.connect(self.on_verify)
        self.btn_attack.clicked.connect(self.on_attack)
        self.btn_collision.clicked.connect(self.on_collision)

    def log(self, message: str):
        self.log_output.append(message)

    def get_key(self) -> str:
        key = self.key_input.text().strip()
        if not key:
            raise ValueError("отсутствует секретный ключ.")
        return key

    def on_load_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Открыть текстовый файл", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_input.setText(content)
                self.log(f"Успешно загружен текст из файла: {file_path}\n")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при чтении файла", str(e))

    def on_save_packet(self):
        try:
            text = self.text_input.text().strip()
            sig = self.sig_input.text().strip()
            if not text or not sig:
                raise ValueError("нет данных для сохранения. Сначала сформируйте HMAC.")

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить пакет данных", "", "JSON Files (*.json)")
            if file_path:
                packet_data = {"data": text, "hmac_hex": sig}
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(packet_data, f, ensure_ascii=False, indent=4)
                self.log(f"Сетевой пакет успешно сохранен в файл: {file_path}\n")
                QMessageBox.information(self, "Успех", "Пакет сохранен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при сохранении файла", str(e))

    def on_create(self):
        try:
            key = self.get_key()
            text = self.text_input.text().strip()
            if not text:
                raise ValueError("не передан текст сообщения.")

            self.log(f"Формирование подписи для сообщения: '{text}'")
            hmac_hex = create.create(text, key)
            packet.transmit_packet(text, hmac_hex)
            
            self.sig_input.setText(hmac_hex)
            self.log(f"Сгенерированный HMAC-SHA256: {hmac_hex}\n")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def on_verify(self):
        try:
            key = self.get_key()
            text = self.text_input.text().strip()
            sig = self.sig_input.text().strip()
            if not text or not sig:
                raise ValueError("для верификации необходимы и текст, и подпись.")

            self.log("Запуск проверки целостности данных...")
            received_packet = {"data": text, "hmac_hex": sig}
            is_valid = packet.verify_packet(received_packet, key)
            
            if is_valid:
                self.log("Проверка успешна. Целостность данных подтверждена, изменений не обнаружено.\n")
                QMessageBox.information(self, "Успех", "Данные подлинные.")
            else:
                self.log("Внимание!!! Обнаружено изменение данных. Цифровая подпись пакета не совпадает.\n")
                QMessageBox.warning(self, "Внимание", "Данные изменены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def on_attack(self):
        try:
            key = self.get_key()
            text = self.text_input.text().strip()
            if not text:
                raise ValueError("не указан новый текст для подмены.")

            self.log("Запуск симуляции компрометации пакета...")
            original_packet = atak.get_original_packet(key)

            spoiled_packet = atak.simulate_atak(original_packet, text)
            self.log(f"Хакер подменил текст на: '{text}'")
            
            is_spoiled_valid = packet.verify_packet(spoiled_packet, key)
            if is_spoiled_valid:
                self.log("Критический сбой системы защиты.\n")
            else:
                self.log("Внимание!!! Обнаружено изменение данных. Цифровая подпись пакета не совпадает.\n")
                QMessageBox.warning(self, "Детектор атак", "Обнаружена атака!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def on_collision(self):
        try:
            key = self.get_key()
            self.log("Запуск процесса подбора коллизии для усеченного HMAC...")
            self.log("Прогресс перебора отображается в консоли терминала.")
            
            QApplication.setOverrideCursor(Qt.WaitCursor)
            msg1, msg2, shared_hmac = collision.find_collision(key)
            QApplication.restoreOverrideCursor()

            self.log("Коллизия успешно обнаружена!")
            self.log(f"Первое сообщение: {msg1}")
            self.log(f"Второе сообщение: {msg2}")
            self.log(f"Общий усеченный HMAC: {shared_hmac}...\n")
            
            QMessageBox.information(
                self, 
                "Коллизия найдена", 
                f"Найдено совпадение!\n\n1: {msg1}\n2: {msg2}\nHMAC: {shared_hmac}"
            )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HMACApp()
    window.show()
    sys.exit(app.exec_())