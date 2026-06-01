import sys
from PyQt5.QtWidgets import *
from backend import Auth

class AuthApp(QWidget):
    """
    Графический интерфейс пользователя (GUI) для системы аутентификации на PyQt5.
    
    Предоставляет форму для ввода имени пользователя и пароля с возможностью
    выбора метода хеширования (обычный SHA-256 или безопасный bcrypt).
    
    Атрибуты:
        auth (Auth): Экземпляр бэкенда аутентификации
    """
    
    def __init__(self, auth):
        """
        Инициализация GUI приложения.
        
        Аргументы:
            auth (Auth): Объект класса Auth для выполнения операций регистрации и входа
        """
        super().__init__()
        self.auth = auth
        self.init_ui()

    def init_ui(self):
        """
        Создание и размещение всех виджетов интерфейса.
        
        Создаёт:
            - Поле ввода имени пользователя (QLineEdit)
            - Поле ввода пароля (с маскированием символов)
            - Флажок "Use bcrypt" для выбора метода хеширования
            - Кнопки "Register" и "Login"
            
        Примечание:
            Окно имеет размер 400x250 пикселей и заголовок "Auth System".
            Используется вертикальный менеджер компоновки QVBoxLayout.
        """
        self.setWindowTitle("Auth System")
        self.resize(400, 250)

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)  # Маскирование пароля

        self.chk = QCheckBox("Use bcrypt")  # Выбор безопасного хеширования

        btn1 = QPushButton("Register")
        btn2 = QPushButton("Login")

        btn1.clicked.connect(self.register)
        btn2.clicked.connect(self.login)

        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(self.chk)
        layout.addWidget(btn1)
        layout.addWidget(btn2)

        self.setLayout(layout)

    def register(self):
        """
        Обработчик нажатия кнопки регистрации.
        
        Получает данные из полей ввода и вызывает соответствующий метод регистрации
        в зависимости от состояния флажка "Use bcrypt":
            - Флажок установлен: используется безопасная регистрация (bcrypt)
            - Флажок снят: используется небезопасная регистрация (SHA-256)
            
        При успехе показывает информационное сообщение.
        При ошибке показывает предупреждение с текстом исключения.
        """
        u = self.user.text()
        p = self.pwd.text()

        try:
            if self.chk.isChecked():
                self.auth.safe_registration(u, p)
            else:
                self.auth.unsafe_registration(u, p)

            QMessageBox.information(self, "OK", "Registered")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def login(self):
        """
        Обработчик нажатия кнопки входа.
        
        Получает данные из полей ввода и вызывает verify_user() для проверки.
        
        При успешной проверке показывает информационное сообщение "Success".
        При неудаче показывает предупреждение "Wrong credentials".
        """
        u = self.user.text()
        p = self.pwd.text()

        if self.auth.verify_user(u, p):
            QMessageBox.information(self, "OK", "Success")
        else:
            QMessageBox.warning(self, "Fail", "Wrong credentials")

def run_gui(auth):
    """
    Запуск графического интерфейса приложения.
    
    Аргументы:
        auth (Auth): Экземпляр бэкенда аутентификации для передачи в GUI
        
    Примечание:
        Функция создаёт QApplication, главное окно и запускает событийный цикл.
        Завершает работу с кодом выхода из приложения.
    """
    app = QApplication(sys.argv)
    w = AuthApp(auth)
    w.show()
    sys.exit(app.exec_())