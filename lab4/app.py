"""GUI-приложение системы аутентификации на PyQt5."""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTextEdit
)
from auth import register_user, authenticate_user


class AuthApp(QWidget):
    """Главное окно приложения."""

    def __init__(self):
        """Инициализирует окно и создаёт интерфейс."""
        super().__init__()
        self.db_salt = "users_salted.json"
        self.db_nosalt = "users_nosalt.json"
        self.init_ui()

    def init_ui(self):
        """Создаёт графический интерфейс."""
        self.setWindowTitle("Менеджер авторизации")
        self.setMinimumSize(400, 450)

        self.lbl_login = QLabel("Логин:")
        self.txt_login = QLineEdit()
        self.txt_login.setPlaceholderText("От 3 до 20 символов")

        self.lbl_password = QLabel("Пароль:")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)

        self.lbl_mode = QLabel("Режим хранения:")
        self.rad_secure = QRadioButton("Безопасный (с солью)")
        self.rad_secure.setChecked(True)
        self.rad_unsecure = QRadioButton("Небезопасный (без соли)")

        self.group_mode = QButtonGroup()
        self.group_mode.addButton(self.rad_secure)
        self.group_mode.addButton(self.rad_unsecure)

        self.btn_reg = QPushButton("Регистрация")
        self.btn_auth = QPushButton("Войти")

        self.lbl_log = QLabel("Лог работы:")
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_login)
        layout.addWidget(self.txt_login)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.lbl_mode)
        layout.addWidget(self.rad_secure)
        layout.addWidget(self.rad_unsecure)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_reg)
        btn_layout.addWidget(self.btn_auth)
        layout.addLayout(btn_layout)

        layout.addWidget(self.lbl_log)
        layout.addWidget(self.txt_log)

        self.setLayout(layout)

        self.btn_reg.clicked.connect(self.handle_registration)
        self.btn_auth.clicked.connect(self.handle_authorization)

    def log(self, text: str):
        """Добавляет сообщение в лог.

        Args:
            text (str): Текст сообщения.
        """
        self.txt_log.append(text)

    def get_inputs(self) -> tuple:
        """Получает и проверяет данные из полей ввода.

        Returns:
            tuple: (login, password, is_secure) или (None, None, None)
            при ошибке.
        """
        login = self.txt_login.text().strip()
        password = self.txt_password.text()
        is_secure = self.rad_secure.isChecked()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return None, None, None

        if len(login) < 3 or len(login) > 20:
            QMessageBox.warning(self, "Ошибка", "Логин должен быть от 3 до 20 символов!")
            return None, None, None

        return login, password, is_secure

    def handle_registration(self):
        """Обрабатывает нажатие кнопки регистрации."""
        login, password, is_secure = self.get_inputs()
        if not login:
            return

        db_path = self.db_salt if is_secure else self.db_nosalt
        mode_name = "Безопасный" if is_secure else "Небезопасный"
        self.log(f"Режим: {mode_name} регистрация")

        try:
            result = register_user(login, password, db_path, use_salt=is_secure)
            self.log(result)
            if "успешно" in result:
                QMessageBox.information(self, "Успех", result)
            else:
                QMessageBox.warning(self, "Ошибка", result)
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
            QMessageBox.critical(self, "Ошибка", str(e))

    def handle_authorization(self):
        """Обрабатывает нажатие кнопки авторизации."""
        login, password, is_secure = self.get_inputs()
        if not login:
            return

        db_path = self.db_salt if is_secure else self.db_nosalt
        mode_name = "Безопасный" if is_secure else "Небезопасный"
        self.log(f"Режим: {mode_name} авторизация")

        try:
            result = authenticate_user(login, password, db_path, use_salt=is_secure)
            self.log(result)
            if "Добро пожаловать" in result:
                QMessageBox.information(self, "Успех", result)
            else:
                QMessageBox.warning(self, "Ошибка", result)
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec_())