import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QRadioButton, QButtonGroup, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt

from hash_units import generate_salt, calculate_hash
from file_units import write_json_file, safe_load_database
from checks import check_login, check_secure_user_data, check_unsecure_user_data


DB_SALT = "users_salted.json"
DB_NOSALT = "users_nosalt.json"


class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Менеджер авторизации")
        self.setMinimumSize(400, 450)

        # Поля ввода
        self.lbl_login = QLabel("Логин:")
        self.txt_login = QLineEdit()
        self.txt_login.setPlaceholderText("От 3 до 20 символов")

        self.lbl_password = QLabel("Пароль:")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Выбор режима безопасности
        self.lbl_mode = QLabel("Режим хранения:")
        self.rad_secure = QRadioButton("Безопасный (с солью)")
        self.rad_secure.setChecked(True)
        self.rad_unsecure = QRadioButton("Небезопасный (без соли)")
        
        self.group_mode = QButtonGroup()
        self.group_mode.addButton(self.rad_secure)
        self.group_mode.addButton(self.rad_unsecure)

        # Кнопки действий
        self.btn_reg = QPushButton("Регистрация")
        self.btn_auth = QPushButton("Войти")

        # Поле вывода логов/результатов
        self.lbl_log = QLabel("Лог работы:")
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)

        # Компоновка интерфейса (Layouts)
        layout = QVBoxLayout()
        
        layout.addWidget(self.lbl_login)
        layout.addWidget(self.txt_login)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        
        layout.addWidget(self.lbl_mode)
        layout.addWidget(self.rad_secure)
        layout.addWidget(self.rad_unsecure)
        
        # Горизонтальная линия для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_reg)
        btn_layout.addWidget(self.btn_auth)
        layout.addLayout(btn_layout)
        
        layout.addWidget(self.lbl_log)
        layout.addWidget(self.txt_log)

        self.setLayout(layout)

        # Подключение обработчиков событий
        self.btn_reg.clicked.connect(self.handle_registration)
        self.btn_auth.clicked.connect(self.handle_authorization)


    def log(self, text):
        """Вывод сообщений в текстовое поле интерфейса."""
        self.txt_log.append(text)


    def get_inputs(self):
        """Получение и валидация базовых данных из полей ввода."""
        login = self.txt_login.text().strip()
        password = self.txt_password.text()
        is_secure = self.rad_secure.isChecked()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return None, None, None

        # Используем вашу функцию проверки логина
        if not check_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин не соответствует требованиям (3-20 символов)!")
            return None, None, None

        return login, password, is_secure


    def handle_registration(self):
        login, password, is_secure = self.get_inputs()
        if not login:
            return

        if is_secure:
            self.log("Режим: Безопасная регистрация")
            db_file = DB_SALT
            database = safe_load_database(db_file)
            if database is None:
                self.log("Ошибка: Не удалось загрузить БД.")
                return

            if login in database:
                self.log("Пользователь с таким именем уже существует.")
                QMessageBox.warning(self, "Ошибка", "Пользователь уже существует.")
                return

            salt = generate_salt()
            password_hash = calculate_hash(password, salt)

            database[login] = {"hash": password_hash, "salt": salt}
            write_json_file(db_file, database)
            self.log(f"Добро пожаловать в безопасный клуб, {login}!\n")
            QMessageBox.information(self, "Успех", f"Пользователь {login} зарегистрирован!")
        else:
            self.log("Режим: Небезопасная регистрация")
            db_file = DB_NOSALT
            database = safe_load_database(db_file)
            if database is None:
                self.log("Ошибка: Не удалось загрузить БД.")
                return

            if login in database:
                self.log("Пользователь с таким именем уже существует.")
                QMessageBox.warning(self, "Ошибка", "Пользователь уже существует.")
                return

            password_hash = calculate_hash(password)
            database[login] = password_hash
            write_json_file(db_file, database)
            self.log(f"Добро пожаловать в небезопасный клуб, {login}!\n")
            QMessageBox.information(self, "Успех", f"Пользователь {login} зарегистрирован!")


    def handle_authorization(self):
        login, password, is_secure = self.get_inputs()
        if not login:
            return

        if is_secure:
            self.log("Режим: Безопасная авторизация")
            database = safe_load_database(DB_SALT)
            if database is None:
                return

            if len(database) == 0:
                self.log("В системе нет зарегистрированных пользователей.")
                return

            if login not in database:
                self.log("Такого пользователя нет в базе данных.")
                return

            user_info = database[login]
            if not check_secure_user_data(user_info, login):
                self.log("Ошибка целостности данных пользователя.")
                return

            user_salt = user_info["salt"]
            old_password_hash = user_info["hash"]
            new_password_hash = calculate_hash(password, user_salt)

            if old_password_hash == new_password_hash:
                self.log(f"С возвращением в безопасный клуб, {login}!\n")
                QMessageBox.information(self, "Успех", "Авторизация успешна!")
            else:
                self.log(f"Пароль не подходит для логина {login}.\n")
                QMessageBox.critical(self, "Ошибка", "Неверный пароль!")
        else:
            self.log("Режим: Небезопасная авторизация")
            database = safe_load_database(DB_NOSALT)
            if database is None:
                return

            if len(database) == 0:
                self.log("В системе нет зарегистрированных пользователей.")
                return

            if login not in database:
                self.log("Такого пользователя нет в базе данных.")
                return

            old_password_hash = database[login]
            if not check_unsecure_user_data(old_password_hash, login):
                self.log("Ошибка целостности данных пользователя.")
                return

            new_password_hash = calculate_hash(password)

            if old_password_hash == new_password_hash:
                self.log(f"С возвращением в небезопасный клуб, {login}!\n")
                QMessageBox.information(self, "Успех", "Авторизация успешна!")
            else:
                self.log(f"Пароль не подходит для логина {login}.\n")
                QMessageBox.critical(self, "Ошибка", "Неверный пароль!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.argv = [""]
    sys.exit(app.exec())
