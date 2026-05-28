"""
Главное приложение (PyQt5).
"""

import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QMessageBox
)

from symmetric_cipher import SymmetricCipher
from asymmetric_cipher import AsymmetricCipher
from key_generator import KeyGenerator
from file_manager import FileManager


class MainWindow(QWidget):
    """Главное окно приложения."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Гибридная система — SEED + RSA")
        self.resize(500, 400)
        self.init_ui()

    def _load_settings(self) -> dict:
        """Загружает настройки из JSON. Если файла нет — программа завершается."""
        try:
            return FileManager.load_json("settings.json")
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "settings.json не найден. Программа будет закрыта.")
            sys.exit(1)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Ошибка формата JSON. Программа будет закрыта.")
            sys.exit(1)

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        btn_gen = QPushButton("1. Генерация ключей")
        btn_gen.clicked.connect(self.safe_generate)

        btn_enc = QPushButton("2. Шифрование")
        btn_enc.clicked.connect(self.safe_encrypt)

        btn_dec = QPushButton("3. Дешифрование")
        btn_dec.clicked.connect(self.safe_decrypt)

        layout.addWidget(btn_gen)
        layout.addWidget(btn_enc)
        layout.addWidget(btn_dec)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def log_message(self, message: str) -> None:
        self.log.append(message)

    def safe_generate(self) -> None:
        try:
            settings = self._load_settings()
            KeyGenerator.generate(settings, self.log_message)
            QMessageBox.information(self, "Успех", "Ключи созданы.")
        except Exception as exc:
            self.handle_error(exc)

    def safe_encrypt(self) -> None:
        try:
            settings = self._load_settings()
            encrypted_key = FileManager.read(settings["symmetric_key"])
            symmetric_key = AsymmetricCipher.decrypt(
                encrypted_key,
                Path(settings["private_key"])
            )

            self.log_message("SEED ключ расшифрован.")

            data = FileManager.read(settings["initial_file"])
            encrypted = SymmetricCipher.encrypt(
                data,
                symmetric_key,
                settings["seed_block_size"],
                settings["seed_key_size"]
            )
            FileManager.write(settings["encrypted_file"], encrypted)

            self.log_message("Файл успешно зашифрован.")
            QMessageBox.information(self, "Успех", "Файл зашифрован.")
        except Exception as exc:
            self.handle_error(exc)

    def safe_decrypt(self) -> None:
        try:
            settings = self._load_settings()
            encrypted_key = FileManager.read(settings["symmetric_key"])
            symmetric_key = AsymmetricCipher.decrypt(
                encrypted_key,
                Path(settings["private_key"])
            )

            self.log_message("SEED ключ расшифрован.")

            encrypted_data = FileManager.read(settings["encrypted_file"])
            decrypted = SymmetricCipher.decrypt(
                encrypted_data,
                symmetric_key,
                settings["seed_block_size"],
                settings["seed_key_size"]
            )
            FileManager.write(settings["decrypted_file"], decrypted)

            self.log_message("Файл успешно расшифрован.")
            QMessageBox.information(self, "Успех", "Файл расшифрован.")
        except Exception as exc:
            self.handle_error(exc)

    def handle_error(self, error: Exception) -> None:
        self.log_message(f"Ошибка: {error}")
        QMessageBox.critical(self, "Ошибка", str(error))


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
