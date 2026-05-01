import sys
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFileDialog,
    QRadioButton, QMessageBox
)

from crypto_service import encrypt_file, decrypt_file, generate_all_keys


class HybridCryptoSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = self.load_settings()
        self.input_fields = {}

        self.setup_ui()
        self.fill_fields_from_settings()


    def load_settings(self):
        """Загрузка настроек из JSON файла."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def fill_fields_from_settings(self):
        """Заполнение полей данными с настроек"""
        for key, field in self.input_fields.items():
            if key in self.settings:
                field.setText(self.settings[key])

    def collect_input_data(self):
        """Собирание данных с интерфейса."""
        data = {}
        for key, field in self.input_fields.items():
            data[key] = field.text().strip()
        return data


    def setup_ui(self):
        self.setWindowTitle("Hybrid Crypto Tool")
        self.setMinimumSize(580, 320)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.encrypt_mode = QRadioButton("Шифрование")
        self.decrypt_mode = QRadioButton("Дешифрование")
        self.encrypt_mode.setChecked(True)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.encrypt_mode)
        mode_layout.addWidget(self.decrypt_mode)
        main_layout.addLayout(mode_layout)

        field_definitions = [
            ("initial_file", "Input file"),
            ("encrypted_file", "Encrypted file"),
            ("decrypted_file", "Decrypted file"),
            ("public_key", "Public key"),
            ("secret_key", "Private key"),
            ("symmetric_key", "Symmetric key"),
            ("nonce", "Nonce"),
            ("encrypted_symmetric_key", "Encrypted key"),
        ]

        for key, label_text in field_definitions:
            row_layout = QHBoxLayout()

            label = QLabel(label_text)
            label.setMinimumWidth(140)

            line_edit = QLineEdit()
            button = QPushButton("...")

            button.clicked.connect(lambda _, k=key: self.open_file_dialog(k))

            row_layout.addWidget(label)
            row_layout.addWidget(line_edit)
            row_layout.addWidget(button)

            main_layout.addLayout(row_layout)
            self.input_fields[key] = line_edit

        button_layout = QHBoxLayout()

        run_button = QPushButton("Выполнить")
        run_button.clicked.connect(self.run_operation)

        generate_button = QPushButton("Создать ключи")
        generate_button.clicked.connect(self.generate_keys)

        button_layout.addWidget(run_button)
        button_layout.addWidget(generate_button)

        main_layout.addLayout(button_layout)

        self.status_label = QLabel("Готовность")
        main_layout.addWidget(self.status_label)



    def open_file_dialog(self, key):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if path:
            self.input_fields[key].setText(path)


    def validate_input(self, required_keys, data):
        """Проверка ввода пользователя."""
        for key in required_keys:
            path = data.get(key)

            if not path:
                raise ValueError(f"Поле '{key}' пустое")

            try:
                with open(path, "rb"):
                    pass
            except:
                raise FileNotFoundError(f"Файл не найден: {path}")


    def run_operation(self):
        """Выполнение операции шифрования или дешифрования."""
        data = self.collect_input_data()

        try:
            if self.encrypt_mode.isChecked():
                self.validate_input(
                    ["initial_file", "public_key", "symmetric_key", "nonce"],
                    data
                )
                encrypt_file(data)
                self.update_status("Шифрование завершено")

            else:
                self.validate_input(
                    ["encrypted_file", "secret_key", "encrypted_symmetric_key", "nonce"],
                    data
                )
                decrypt_file(data)
                self.update_status("Дешифрованиие завершено")

        except Exception as e:
            self.show_error(str(e))

    def generate_keys(self):
        paths = self.collect_input_data()

        required = ["public_key", "secret_key", "symmetric_key", "nonce"]

        try:
            for key in required:
                if not paths.get(key):
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        f"Поле '{key}' пустое"
                    )
                    return

            generate_all_keys(paths.get("public_key"),
                              paths.get("secret_key"),
                              paths.get("symmetric_key"),
                              paths.get("nonce"),
            )

            self.update_status("Ключи созданы")

        except Exception as e:
            self.show_error(str(e))


    def update_status(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, "Информация", message)

    def show_error(self, message):
        self.status_label.setText("Ошибка")
        QMessageBox.critical(self, "Ошибка", message)


def main():
    app = QApplication(sys.argv)
    window = HybridCryptoSystemApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()