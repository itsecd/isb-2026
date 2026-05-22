import os
import sys
import sqlite3

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from crypto_utils import generate_hash
from SQL import register_user, initSQL, get_user


class AuthWindow(QWidget):
    db_path = "users.db"

    def __init__(self):
        """Constructor of class"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Init UI and sql database"""
        self.setWindowTitle("Авторизация и регистрация")
        self.setFixedSize(700, 300)

        login_group = QGroupBox("Вход в систему")
        login_layout = QVBoxLayout()

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Логин")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Пароль")
        self.login_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.on_login_clicked)

        login_layout.addWidget(QLabel("Логин:"))
        login_layout.addWidget(self.login_username)
        login_layout.addWidget(QLabel("Пароль:"))
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(self.btn_login)
        login_layout.addStretch()
        login_group.setLayout(login_layout)

        register_group = QGroupBox("Регистрация нового пользователя")
        register_layout = QVBoxLayout()

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Придумайте логин")
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Пароль")
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setPlaceholderText("Повторите пароль")
        self.reg_confirm.setEchoMode(QLineEdit.Password)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.clicked.connect(self.on_register_clicked)

        register_layout.addWidget(QLabel("Логин:"))
        register_layout.addWidget(self.reg_username)
        register_layout.addWidget(QLabel("Пароль:"))
        register_layout.addWidget(self.reg_password)
        register_layout.addWidget(QLabel("Подтверждение пароля:"))
        register_layout.addWidget(self.reg_confirm)
        register_layout.addWidget(self.btn_register)
        register_layout.addStretch()
        register_group.setLayout(register_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(login_group, 1)
        main_layout.addWidget(register_group, 1)
        self.setLayout(main_layout)

        initSQL(self.db_path)

    def on_login_clicked(self):
        """Logic when login button clicked"""
        username = self.login_username.text()
        password = self.login_password.text()
        try:
            stored_hash, stored_salt = get_user(username, self.db_path)
        except TypeError:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не существует пользователя '{username}'!",
            )
            return
        if bytes.fromhex(stored_hash) == generate_hash(
            password, bytes.fromhex(stored_salt)
        ):
            QMessageBox.information(
                self,
                "Успех",
                f"Успешный вход пользвателя '{username}'!",
            )
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Неверный логин или пароль!",
            )

    def on_register_clicked(self):
        """Logic when register button clicked"""

        username = self.reg_username.text()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()

        if password != confirm:
            QMessageBox.warning(self, "Ошибка регистрации", "Пароли не совпадают!")
            return

        if not username or not password:
            QMessageBox.warning(
                self, "Ошибка регистрации", "Логин и пароль не могут быть пустыми!"
            )
            return
        try:
            register_user(username, generate_hash(password, b""), b"", self.db_path)

            QMessageBox.information(
                self,
                "Успех",
                f"Пользователь '{username}' успешно зарегистрирован",
            )
        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Пользователь '{username}' уже зарегистрирован",
            )
        except Exception as e:
            print(e)
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Непредвиденная ошибка!",
            )

        self.reg_username.clear()
        self.reg_password.clear()
        self.reg_confirm.clear()


if __name__ == "__main__":
    """Main function. Entry point"""
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())
