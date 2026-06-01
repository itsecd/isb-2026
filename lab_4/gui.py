import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox
from UserManager import UserManager, UserManagerError
import analysator

class AuthApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.manager = UserManager()
        self.init_ui()

    def init_ui(self):
        """
        Инициализация главного окна
        """
        self.setWindowTitle("Лабораторная работа: Хеширование")
        self.resize(400, 300)
        
        layout = QVBoxLayout()

        
        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Введите логин")
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)

        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText("Введите пароль")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.pass_input)

       
        self.algo_chooser = QComboBox(self)
        self.algo_chooser.addItems(["bcrypt", "sha256_salted", "sha256"])
        layout.addWidget(QLabel("Алгоритм хеширования (для регистрации):"))
        layout.addWidget(self.algo_chooser)

        btn_reg = QPushButton("Зарегистрироваться", self)
        btn_reg.clicked.connect(self.handle_register)
        layout.addWidget(btn_reg)

        btn_auth = QPushButton("Войти в систему", self)
        btn_auth.clicked.connect(self.handle_auth)
        layout.addWidget(btn_auth)

        btn_crack = QPushButton("Запустить анализ (Брутфорс в консоли)", self)
        btn_crack.clicked.connect(self.handle_crack)
        layout.addWidget(btn_crack)

        self.setLayout(layout)

    def handle_register(self):
        """
        Обработчик событий регистрации
        """
        try:
            self.manager.register(
                self.login_input.text(), 
                self.pass_input.text(), 
                self.algo_chooser.currentText()
            )
            QMessageBox.information(self, "Успех", "Пользователь зарегистрирован!")
        except UserManagerError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def handle_auth(self):
        """
        Обработчик событий логина
        """
        try:
            success = self.manager.authenticate(self.login_input.text(), self.pass_input.text())
            if success:
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")
            else:
                QMessageBox.warning(self, "Внимание", "Неверный пароль.")
        except UserManagerError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def handle_crack(self):
        """
        Обработчик событий испытаний на уязвимости
        """
        QMessageBox.information(self, "Инфо", "Смотри вывод прогресс-бара в консоли (терминале)!")
        analysator.vuln_analyse("qwerty")
        analysator.vuln_salt_analyse("qwerty")

def run_gui():
    """
    Запускает GUI версию приложения
    """
    app = QApplication(sys.argv)
    window = AuthApp()
    window.show()
    sys.exit(app.exec())