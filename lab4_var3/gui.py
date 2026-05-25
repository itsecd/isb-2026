import sys
import random
import string
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import data_processing
import auth
import auth_no_salt

class BruteForceWorker(QThread):
    progress_changed = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, username, data):
        super().__init__()
        self.username = username
        self.data = data

    def run(self):
        try:
            stored_hash = self.data.get(self.username)
            if not stored_hash:
                self.finished.emit(f"Ошибка: пользователь '{self.username}' не найден.")
                return

            is_no_salt = len(stored_hash) == 64
            max_attempts = 100000 if is_no_salt else 50
            
            chars = string.ascii_lowercase + string.digits
            found_password = None

            for i in range(max_attempts):
                update_step = 1 if not is_no_salt else 100
                
                if i % update_step == 0:
                    progress_percent = int((i / max_attempts) * 100)
                    self.progress_changed.emit(progress_percent)

                length = random.randint(4, 6)
                candidate = "".join(random.choice(chars) for _ in range(length))
                
                if is_no_salt:
                    if auth_no_salt.check_password_no_salt(candidate, stored_hash):
                        found_password = candidate
                        break
                else:
                    if auth.check_password(candidate, stored_hash):
                        found_password = candidate
                        break
                        
            self.progress_changed.emit(100)
            if found_password:
                self.finished.emit(f"Успех: найдена коллизия '{found_password}'")
            else:
                self.finished.emit(f"[FAIL] За {max_attempts} случайных генераций совпадений не найдено.")
        except Exception as e:
            self.finished.emit(f"Ошибка при поиске коллизии: {e}")

class AuthApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система аутентификации")
        self.setMinimumSize(500, 550)
        
        self.settings_path = "settings.json"
        
        if not os.path.exists(self.settings_path):
            data_processing.save_json(self.settings_path, {"path_to_data": "users_db.json"})
            
        config = data_processing.load_json(self.settings_path)
        self.data_path = config.get("path_to_data", "users_db.json")
        
        if not os.path.exists(self.data_path):
            data_processing.save_json(self.data_path, {})

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        mode_label = QLabel("Выберите режим работы:")
        mode_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        main_layout.addWidget(mode_label)

        self.mode_group = QButtonGroup(self)
        
        self.rb_aut = QRadioButton("Аутентификация с солью")
        self.rb_reg = QRadioButton("Регистрация с солью ")
        self.rb_aut_ns = QRadioButton("Аутентификация БЕЗ соли ")
        self.rb_reg_ns = QRadioButton("Регистрация БЕЗ соли ")
        self.rb_dec = QRadioButton("Подбор коллизии ")

        self.rb_aut.setChecked(True)

        self.mode_group.addButton(self.rb_aut)
        self.mode_group.addButton(self.rb_reg)
        self.mode_group.addButton(self.rb_aut_ns)
        self.mode_group.addButton(self.rb_reg_ns)
        self.mode_group.addButton(self.rb_dec)

        rb_layout = QVBoxLayout()
        rb_layout.addWidget(self.rb_aut)
        rb_layout.addWidget(self.rb_reg)
        rb_layout.addWidget(self.rb_aut_ns)
        rb_layout.addWidget(self.rb_reg_ns)
        rb_layout.addWidget(self.rb_dec)
        main_layout.addLayout(rb_layout)

        self.mode_group.buttonToggled.connect(self.handle_mode_change)

        form_layout = QVBoxLayout()
        
        self.user_label = QLabel("Имя пользователя:")
        self.input_user = QLineEdit()
        form_layout.addWidget(self.user_label)
        form_layout.addWidget(self.input_user)

        self.pass_label = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.pass_label)
        form_layout.addWidget(self.input_password)

        main_layout.addLayout(form_layout)

        self.btn_submit = QPushButton("Выполнить")
        self.btn_submit.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; font-weight: bold; padding: 8px;")
        self.btn_submit.clicked.connect(self.process_action)
        main_layout.addWidget(self.btn_submit)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        main_layout.addWidget(QLabel("Консоль вывода:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #1e1e1e; color: #a9b7c6; font-family: monospace; font-size: 12px;")
        main_layout.addWidget(self.log_output)

    def log(self, message: str):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()

    def handle_mode_change(self, button, checked):
        if self.rb_dec.isChecked():
            self.input_password.setEnabled(False)
            self.input_password.setText("")
            self.pass_label.setText("Пароль (не требуется для брутфорса):")
        else:
            self.input_password.setEnabled(True)
            self.pass_label.setText("Пароль:")

    def on_brute_progress(self, value):
        self.progress_bar.setValue(value)

    def on_brute_finished(self, result_message):
        self.log(result_message)
        self.progress_bar.setVisible(False)
        self.btn_submit.setEnabled(True)

    def process_action(self):
        username = self.input_user.text().strip()
        password = self.input_password.text().strip()

        if not username:
            self.log("Введите имя пользователя")
            return

        data = data_processing.load_json(self.data_path)

        if self.rb_aut.isChecked():
            if not password: 
                self.log("Введите пароль")
                return
            if auth.login_user(username, password, data):
                self.log(f"Добро пожаловать, {username}!")
            else:
                self.log("Ошибка: неверные данные.")

        elif self.rb_reg.isChecked():
            if not password: 
                self.log("Введите пароль")
                return
            if auth.register_user(username, password, data):
                data_processing.save_json(self.data_path, data)
                self.log(f"Пользователь '{username}' зарегистрирован.")
            else:
                self.log(f"Ошибка: пользователь '{username}' уже существует.")

        elif self.rb_aut_ns.isChecked():
            if not password: 
                self.log("Введите пароль")
                return
            if auth_no_salt.login_user_no_salt(username, password, data):
                self.log(f"Вход выполнен (БЕЗ СОЛИ): {username}")
            else:
                self.log("Ошибка: неверные данные.")

        elif self.rb_reg_ns.isChecked():
            if not password: 
                self.log("Введите пароль")
                return
            if auth_no_salt.register_user_no_salt(username, password, data):
                data_processing.save_json(self.data_path, data)
                self.log(f"Пользователь '{username}' зарегистрирован (БЕЗ СОЛИ).")
            else:
                self.log(f"Ошибка: пользователь '{username}' уже существует.")

        elif self.rb_dec.isChecked():
            self.btn_submit.setEnabled(False)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            self.log(f"Старт брутфорса для '{username}'...")

            self.worker = BruteForceWorker(username, data)
            self.worker.progress_changed.connect(self.on_brute_progress)
            self.worker.finished.connect(self.on_brute_finished)
            self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec())