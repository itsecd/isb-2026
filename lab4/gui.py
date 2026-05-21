"""Графический интерфейс на PyQt для работы с HMAC."""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox)
from hmac_core import compute_hmac, verify_hmac
from config_loader import DEFAULT_KEY


class HMACGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HMAC - Проверка подлинности сообщений")
        self.setMinimumSize(550, 450)
        self.current_hmac = ""
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Секретный ключ:"))
        self.key_input = QLineEdit()
        self.key_input.setText(DEFAULT_KEY)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        layout.addWidget(QLabel("Сообщение:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(120)
        layout.addWidget(self.message_input)

        self.compute_btn = QPushButton("1. Вычислить HMAC")
        self.compute_btn.clicked.connect(self._on_compute)
        layout.addWidget(self.compute_btn)

        layout.addWidget(QLabel("Вычисленный HMAC:"))
        self.hmac_output = QLineEdit()
        self.hmac_output.setReadOnly(True)
        layout.addWidget(self.hmac_output)

        layout.addWidget(QLabel("─" * 50))

        layout.addWidget(QLabel("HMAC для проверки:"))
        self.hmac_check = QLineEdit()
        layout.addWidget(self.hmac_check)

        self.verify_btn = QPushButton("2. Проверить подлинность")
        self.verify_btn.clicked.connect(self._on_verify)
        layout.addWidget(self.verify_btn)

        self.modify_btn = QPushButton("3. Изменить сообщение (демо подмены)")
        self.modify_btn.clicked.connect(self._on_modify)
        layout.addWidget(self.modify_btn)

    def _get_key(self):
        return self.key_input.text().strip()

    def _get_message(self):
        return self.message_input.toPlainText().strip()

    def _on_compute(self):
        try:
            key = self._get_key()
            message = self._get_message()
            if not key or not message:
                QMessageBox.warning(self, "Ошибка", "Заполните ключ и сообщение")
                return
            self.current_hmac = compute_hmac(message, key)
            self.hmac_output.setText(self.current_hmac)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _on_verify(self):
        try:
            key = self._get_key()
            message = self._get_message()
            expected = self.hmac_check.text().strip()
            if not key or not message or not expected:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля")
                return
            if verify_hmac(message, key, expected):
                QMessageBox.information(self, "Результат", " Подлинность подтверждена")
            else:
                QMessageBox.warning(self, "Результат", " Подлинность не подтверждена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _on_modify(self):
        current = self._get_message()
        modified = current + " [ИЗМЕНЕНО]" if current else "Изменённое сообщение"
        self.message_input.setPlainText(modified)


def run_gui():
    app = QApplication(sys.argv)
    window = HMACGUI()
    window.show()
    sys.exit(app.exec_())