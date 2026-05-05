import sys
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QFileDialog,
    QRadioButton, QMessageBox, QTabWidget,
    QFormLayout, QTextEdit, QGroupBox
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
        """
        Загрузка настроек из JSON файла.

        Returns:
            Словарь с настройками. 
            Возвращает пустой словарь, если файл не найден 
            или произошла ошибка чтения.
        """
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                return {}
        return {}

    def fill_fields_from_settings(self):
        """
        Заполнение полей данными с настроек
        """
        for key, field in self.input_fields.items():
            if key in self.settings:
                field.setText(self.settings[key])

    def collect_input_data(self):
        """
        Сбор данных с интерфейса.

        Returns:
            Словарь, где ключи - названия параметров, 
            а значения - текст из полей ввода.
        """
        data = {}
        for key, field in self.input_fields.items():
            data[key] = field.text().strip()
        return data


    def setup_ui(self):
        self.setWindowTitle("Гибридная криптосистема")
        self.resize(700, 400)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        tabs.addTab(self.build_files_tab(), "Файлы")
        tabs.addTab(self.build_actions_tab(), "Операции")
        tabs.addTab(self.build_keys_tab(), "Ключи")

        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.status.setMaximumHeight(80)
        tabs.setCornerWidget(self.status)

    def build_files_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        form = QFormLayout()

        file_fields = [
            ("initial_file", "Исходный файл"),
            ("encrypted_file", "Зашифрованный файл"),
            ("decrypted_file", "Расшифрованный файл"),
        ]

        for key, text in file_fields:
            line = QLineEdit()
            btn = QPushButton("...")

            btn.clicked.connect(lambda _, k=key: self.open_file_dialog(k))

            box = QWidget()
            row = QHBoxLayout(box)
            row.addWidget(line)
            row.addWidget(btn)

            form.addRow(QLabel(text), box)
            self.input_fields[key] = line

        layout.addLayout(form)
        return w

    def build_actions_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.encrypt_mode = QRadioButton("Шифрование")
        self.decrypt_mode = QRadioButton("Дешифрование")
        self.encrypt_mode.setChecked(True)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.encrypt_mode)
        mode_layout.addWidget(self.decrypt_mode)

        run_button = QPushButton("Выполнить")
        run_button.clicked.connect(self.run_operation)

        layout.addLayout(mode_layout)
        layout.addWidget(run_button)
        layout.addStretch()

        return w

    def build_keys_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        group = QGroupBox("Ключи")
        form = QFormLayout()

        self.input_fields["public_key"] = QLineEdit()
        b1 = QPushButton("...")
        b1.clicked.connect(lambda: self.open_file_dialog("public_key"))

        r1 = QWidget()
        l1 = QHBoxLayout(r1)
        l1.addWidget(self.input_fields["public_key"])
        l1.addWidget(b1)
        form.addRow("Публичный ключ", r1)

        self.input_fields["secret_key"] = QLineEdit()
        b2 = QPushButton("...")
        b2.clicked.connect(lambda: self.open_file_dialog("secret_key"))

        r2 = QWidget()
        l2 = QHBoxLayout(r2)
        l2.addWidget(self.input_fields["secret_key"])
        l2.addWidget(b2)
        form.addRow("Приватный ключ", r2)

        rest = [
            ("symmetric_key", "Симметричный ключ"),
            ("nonce", "Nonce"),
            ("encrypted_symmetric_key", "Зашифрованный ключ"),
        ]

        for key, text in rest:
            line = QLineEdit()
            btn = QPushButton("...")

            btn.clicked.connect(lambda _, k=key: self.open_file_dialog(k))

            box = QWidget()
            lay = QHBoxLayout(box)
            lay.addWidget(line)
            lay.addWidget(btn)

            match key:
                case "symmetric_key":
                    label = "Симметричный ключ"
                case "nonce":
                    label = "Nonce"
                case _:
                    label = "Зашифрованный ключ"

            form.addRow(label, box)
            self.input_fields[key] = line

        group.setLayout(form)

        gen_button = QPushButton("Создать ключи")
        gen_button.clicked.connect(self.generate_keys)

        layout.addWidget(group)
        layout.addWidget(gen_button)

        return w


    def open_file_dialog(self, key):
        """
        Обработка диалогового окна.

        Args:
            key: Ключ поля ввода, в которое будет записан путь к файлу.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if path:
            self.input_fields[key].setText(path)

    def validate_input(self, required_keys, data):
        """
        Проверка ввода пользователя.

        Проверяет пути в полях, существование и доступность файла

        Args:
            required_keys: Список ключей, обязательных для операции.
            data: Словарь с данными из полей ввода.

        Raises:
            ValueError: Поле с путем пустое.
            FileNotFoundError: Файл не найден.
            PermissionError: Нет доступа к файлу.
            RuntimeError: Ошибка при чтении.
        """
        for key in required_keys:
            path = data.get(key)

            if not path:
                raise ValueError(f"Поле '{key}' пустое")

            try:
                with open(path, "rb"):
                    pass
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {path}")
            except PermissionError:
                raise PermissionError(f"Нет доступа к чтению файла: {path}")
            except Exception as e:
                raise RuntimeError(f"Критическая ошибка при чтении файла: {e}")



    def run_operation(self):
        """
        Выполнение операции шифрования или дешифрования.
        """
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
        """
        Сбор данных и генерация всех ключей.
        """
        paths = self.collect_input_data()

        try:
            if not paths.get("public_key") or not paths.get("secret_key"):
                QMessageBox.warning(self, "Предупреждение", "Нет путей для RSA ключей")
                return

            if not paths.get("symmetric_key"):
                QMessageBox.warning(self, "Предупреждение", "Нет симметричного ключа")
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
        """
        Отображение сообщения статуса и информационного окна.

        Args:
            message (str): Текст сообщения.
        """
        self.status.append(message)
        QMessageBox.information(self, "Информация", message)

    def show_error(self, message):
        """
        Отображение сообщения ошибки и её окна.

        Args:
            message (str): Текст сообщения.
        """
        self.status.append("Ошибка: " + message)
        QMessageBox.critical(self, "Ошибка", message)


def main():
    app = QApplication(sys.argv)
    window = HybridCryptoSystemApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
