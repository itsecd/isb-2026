"""Графический интерфейс на PyQt для работы с HMAC."""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from hmac_core import compute_hmac, verify_hmac
from constants import DEFAULT_KEY


class HMACGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HMAC - Проверка подлинности сообщений")
        self.setMinimumSize(550, 450)
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Поле для ключа
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Секретный ключ:"))
        self.key_input = QLineEdit()
        self.key_input.setText(DEFAULT_KEY)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # Сообщение
        layout.addWidget(QLabel("Сообщение:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(120)
        layout.addWidget(self.message_input)

        # Кнопка вычисления HMAC
        self.compute_btn = QPushButton("1. Вычислить HMAC")
        self.compute_btn.clicked.connect(self._on_compute)
        layout.addWidget(self.compute_btn)

        # Вывод HMAC
        layout.addWidget(QLabel("Вычисленный HMAC:"))
        self.hmac_output = QLineEdit()
        self.hmac_output.setReadOnly(True)
        layout.addWidget(self.hmac_output)

        # Разделитель
        layout.addWidget(QLabel("─" * 50))

        # Поле для ввода HMAC для проверки
        layout.addWidget(QLabel("HMAC для проверки (вставьте или введите):"))
        self.hmac_check = QLineEdit()
        layout.addWidget(self.hmac_check)

        # Кнопка проверки
        self.verify_btn = QPushButton("2. Проверить подлинность")
        self.verify_btn.clicked.connect(self._on_verify)
        layout.addWidget(self.verify_btn)

        # Кнопка для демонстрации изменения данных
        self.modify_btn = QPushButton("3. Изменить сообщение (демо подмены)")
        self.modify_btn.clicked.connect(self._on_modify)
        layout.addWidget(self.modify_btn)

    def _get_key(self) -> str:
        return self.key_input.text().strip()

    def _get_message(self) -> str:
        return self.message_input.toPlainText().strip()

    def _on_compute(self):
        try:
            key = self._get_key()
            message = self._get_message()
            if not key:
                QMessageBox.warning(self, "Ошибка", "Введите секретный ключ")
                return
            if not message:
                QMessageBox.warning(self, "Ошибка", "Введите сообщение")
                return
            hmac_val = compute_hmac(message, key)
            self.hmac_output.setText(hmac_val)
            QMessageBox.information(self, "Успех", "HMAC вычислен! Скопируйте его для проверки.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _on_verify(self):
        try:
            key = self._get_key()
            message = self._get_message()
            expected = self.hmac_check.text().strip()

            if not key:
                QMessageBox.warning(self, "Ошибка", "Введите секретный ключ")
                return
            if not message:
                QMessageBox.warning(self, "Ошибка", "Введите сообщение")
                return
            if not expected:
                QMessageBox.warning(self, "Ошибка", "Введите HMAC для проверки")
                return

            is_valid = verify_hmac(message, key, expected)

            if is_valid:
                QMessageBox.information(self, "Результат", "ПОДЛИННОСТЬ ПОДТВЕРЖДЕНА!\nСообщение не изменялось.")
            else:
                QMessageBox.warning(self, "Результат", "ПОДЛИННОСТЬ НЕ ПОДТВЕРЖДЕНА!\nСообщение было изменено или ключ неверен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _on_modify(self):
        """Демонстрация изменения данных — добавляем точку в конец."""
        current = self._get_message()
        if current:
            modified = current + " [ИЗМЕНЕНО]"
        else:
            modified = "Изменённое сообщение для демонстрации"
        self.message_input.setPlainText(modified)
        QMessageBox.information(
            self, "Демо", 
            "Сообщение изменено!\n"
            "Теперь нажмите 'Проверить подлинность'.\n"
            "HMAC не совпадёт, так как данные были подменены."
        )


def run_gui():
    app = QApplication(sys.argv)
    window = HMACGUI()
    window.show()
    sys.exit(app.exec_())