"""
PyQt6 интерфейс для работы с HMAC.
"""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from crypto_engine import build_hmac, check_hmac
from settings import DEFAULT_SECRET


class HmacWindow(QMainWindow):
    """
    Главное окно приложения.
    """

    def __init__(self):
        super().__init__()

        self.current_signature = ""

        self.setWindowTitle("HMAC SHA-256")
        self.resize(600, 450)

        self.build_ui()

    def build_ui(self) -> None:

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)

        layout.addWidget(QLabel("Секретный ключ"))

        self.key_input = QLineEdit()
        self.key_input.setText(DEFAULT_SECRET)

        layout.addWidget(self.key_input)

        layout.addWidget(QLabel("Сообщение"))

        self.message_input = QTextEdit()

        layout.addWidget(self.message_input)

        generate_button = QPushButton("Вычислить HMAC")
        generate_button.clicked.connect(self.generate_signature)

        layout.addWidget(generate_button)

        self.signature_output = QLineEdit()
        self.signature_output.setReadOnly(True)

        layout.addWidget(self.signature_output)

        verify_button = QPushButton("Проверить сообщение")
        verify_button.clicked.connect(self.verify_signature)

        layout.addWidget(verify_button)

        modify_button = QPushButton("Изменить сообщение")
        modify_button.clicked.connect(self.modify_message)

        layout.addWidget(modify_button)

    def generate_signature(self) -> None:

        try:
            text = self.message_input.toPlainText()
            key = self.key_input.text()

            self.current_signature = build_hmac(text, key)

            self.signature_output.setText(self.current_signature)

        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def verify_signature(self) -> None:

        try:
            result = check_hmac(
                self.message_input.toPlainText(),
                self.key_input.text(),
                self.current_signature,
            )

            if result:
                QMessageBox.information(self, "Результат", "Сообщение подлинное")

            else:
                QMessageBox.warning(self, "Результат", "Данные были изменены")

        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def modify_message(self) -> None:

        current = self.message_input.toPlainText()

        self.message_input.setText(current + " [ИЗМЕНЕНО]")


def run_interface() -> None:
    """
    Запуск PyQt интерфейса.
    """

    app = QApplication(sys.argv)

    window = HmacWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_interface()
