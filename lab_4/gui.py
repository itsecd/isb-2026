import sys
from PyQt5.QtWidgets import(QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from hmac_core import generate_hmac, verify_hmac

class HMACWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("HMAC-SHA256")
        self.setGeometry(300,200,700,500)
        self.message_label = QLabel("Сообщение:")
        self.message_input = QTextEdit()

        self.key_label = QLabel("Секретный ключ:")
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)

        self.hmac_label = QLabel("HMAC-SHA256:")
        self.hmac_input = QTextEdit()

        self.generate_button = QPushButton("Сформировать HMAC")
        self.verify_button = QPushButton("Проверить HMAC")

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.hmac_label)
        layout.addWidget(self.hmac_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.verify_button)

        self.setLayout(layout)

        self.generate_button.clicked.connect(self.generate_hmac_clicked)
        self.verify_button.clicked.connect(self.verify_hmac_clicked)


    def generate_hmac_clicked(self) -> None:
        try:
            message = self.message_input.toPlainText()
            key = self.key_input.text()
            mac = generate_hmac(message, key)
            self.hmac_input.setPlainText(mac)
            QMessageBox.information(self, "Успешно", "HMAC-SHA256 был успешно сформирован.")
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))


    def verify_hmac_clicked(self) -> None:
        try:
            message = self.message_input.toPlainText()
            key = self.key_input.text()
            received_hmac = self.hmac_input.toPlainText()
            is_valid = verify_hmac(message, key, received_hmac)
            if is_valid:
                QMessageBox.information(self, "Результат проверки", "КОРРЕКТНО: сообщение подлинное и не было изменено.")
            else:
                QMessageBox.warning(self,"Результат проверки","НЕКОРРЕКТНО: сообщение, ключ или HMAC указаны неверно.")
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))


def main() -> None:
    app = QApplication(sys.argv)
    window = HMACWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()