"""
Главное приложение (PyQt5).
"""

import json
import sys
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
        """
        Args: None

        Returns: None
        """
        super().__init__()
        self.setWindowTitle("Гибридная система — SEED + RSA")
        self.resize(500, 400)
        self.settings = self.load_settings()
        self.init_ui()

    def load_settings(self) -> dict:
        """
        Args: None

        Returns:
            dict - настройки из файла

        Raises:
            SystemExit: ошибка загрузки
        """
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "settings.json не найден.")
            sys.exit(1)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Ошибка формата JSON.")
            sys.exit(1)

    def init_ui(self) -> None:
        """Args: None Returns: None"""
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
        """
        Args:
            message: str - сообщение для лога

        Returns: None
        """
        self.log.append(message)

    def safe_generate(self) -> None:
        """Args: None Returns: None"""
        try:
            KeyGenerator.generate(self.settings, self.log_message)
            QMessageBox.information(self, "Успех", "Ключи созданы.")
        except Exception as exc:
            self.handle_error(exc)

    def safe_encrypt(self) -> None:
        """Args: None Returns: None"""
        try:
            encrypted_key = FileManager.read(self.settings["symmetric_key"])
            symmetric_key = AsymmetricCipher.decrypt(
                encrypted_key,
                Path(self.settings["private_key"])
            )

            self.log_message("SEED ключ расшифрован.")

            data = FileManager.read(self.settings["initial_file"])
            encrypted = SymmetricCipher.encrypt(
                data,
                symmetric_key,
                self.settings["seed_block_size"],
                self.settings["seed_key_size"]
            )
            FileManager.write(self.settings["encrypted_file"], encrypted)

            self.log_message("Файл успешно зашифрован.")

        except Exception as exc:
            self.handle_error(exc)

    def safe_decrypt(self) -> None:
        """Args: None Returns: None"""
        try:
            encrypted_key = FileManager.read(self.settings["symmetric_key"])
            symmetric_key = AsymmetricCipher.decrypt(
                encrypted_key,
                Path(self.settings["private_key"])
            )

            self.log_message("SEED ключ расшифрован.")

            encrypted_data = FileManager.read(self.settings["encrypted_file"])
            decrypted = SymmetricCipher.decrypt(
                encrypted_data,
                symmetric_key,
                self.settings["seed_block_size"],
                self.settings["seed_key_size"]
            )
            FileManager.write(self.settings["decrypted_file"], decrypted)

            self.log_message("Файл успешно расшифрован.")

        except Exception as exc:
            self.handle_error(exc)

    def handle_error(self, error: Exception) -> None:
        """
        Args:
            error: Exception - ошибка

        Returns: None
        """
        self.log_message(f"Ошибка: {error}")
        QMessageBox.critical(self, "Ошибка", str(error))


def main() -> None:
    """Args: None Returns: None"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()