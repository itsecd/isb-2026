# This Python file uses the following encoding: utf-8
import sys
import os
import argparse

from stylehelper import stylehelper
import database
import hash
import without_salt

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self,path,mode, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        database.init_database(path)
        self.path = path
        self.mode = mode
        self.ui.setupUi(self)
        self.design()
        self.signals()

    def signals(self):
        """Обработка сигналов"""
        self.ui.pushbutton_login.clicked.connect(self.check_lines)
        self.ui.pushbutton_signup.clicked.connect(self.check_lines)
        self.ui.lineEdit_login.textChanged.connect(self.clear_line_l)
        self.ui.lineEdit_password.textChanged.connect(self.clear_line_p)
        self.ui.lineEdit_login_2.textChanged.connect(self.clear_line_l)
        self.ui.lineEdit_password_2.textChanged.connect(self.clear_line_p)
        self.ui.lineEdit_password_confirm.textChanged.connect(self.clear_line_p_c)
        self.ui.pushbutton_signup_1.clicked.connect(self.signup)
        self.ui.pushbutton_signin.clicked.connect(self.signin)

    def check_lines(self):
        """
        Проверяет заполненность полей ввода на текущей вкладке.

        Вызывается по сигналам нажатия кнопок Login и Signup.
        """
        index = self.ui.tabWidget.currentIndex()
        if index==0:
            text_l=self.ui.lineEdit_login.text()
            text_p=self.ui.lineEdit_password.text()
            if not text_l:
                self.ui.lineEdit_login.setStyleSheet("border-color:red;")
                self.ui.lineEdit_login.setPlaceholderText("Login line is empty")
                self.ui.lineEdit_login.setFocus()
                return
            if not text_p:
                self.ui.lineEdit_password.setStyleSheet("border-color:red;")
                self.ui.lineEdit_password.setPlaceholderText("Password line is empty")
                self.ui.lineEdit_password.setFocus()
                return
            self.login_button(text_l,text_p)
        else:
            text_l=self.ui.lineEdit_login_2.text()
            text_p=self.ui.lineEdit_password_2.text()
            text_p_c=self.ui.lineEdit_password_confirm.text()
            if not text_l:
                self.ui.lineEdit_login_2.setStyleSheet("border-color:red;")
                self.ui.lineEdit_login_2.setPlaceholderText("Login line is empty")
                self.ui.lineEdit_login_2.setFocus()
                return
            if not text_p:
                self.ui.lineEdit_password_2.setStyleSheet("border-color:red;")
                self.ui.lineEdit_password_2.setPlaceholderText("Password line is empty")
                self.ui.lineEdit_password_2.setFocus()
                return
            if not text_p_c:
                self.ui.lineEdit_password_confirm.setStyleSheet("border-color:red;")
                self.ui.lineEdit_password_confirm.setPlaceholderText("Confirm your password")
                self.ui.lineEdit_password_confirm.setFocus()
                return
            if text_p_c!=text_p:
                self.ui.lineEdit_password_confirm.clear()
                self.ui.lineEdit_password_confirm.setStyleSheet("border-color:red;")
                self.ui.lineEdit_password_confirm.setPlaceholderText("Passwords don't match")
                self.ui.lineEdit_password_confirm.setFocus()
                return
            self.signup_button(text_l,text_p)

    def clear_line_l(self):
        """Очищает стили у полей ввода логина на обеих вкладках."""
        self.ui.lineEdit_login.setStyleSheet("")
        self.ui.lineEdit_login_2.setStyleSheet("")
    def clear_line_p(self):
        """Очищает стили у полей ввода пароля на обеих вкладках."""
        self.ui.lineEdit_password.setStyleSheet("")
        self.ui.lineEdit_password_2.setStyleSheet("")
    def clear_line_p_c(self):
        """Очищает стили у поля подтверждения пароля на вкладке регистрации."""
        self.ui.lineEdit_password_confirm.setStyleSheet("")

    def login_button(self,text_l,text_p):
        """
        Вход пользователя по логину и паролю.

        Ищет пользователя в базе данных. Если найден — сравнивает введённый пароль
        с сохранённым хешем, используя соответствующий режим (с солью или без).
        Выводит сообщение об успехе или неудаче.

        Args:
            text_l (str): Логин пользователя.
            text_p (str): Пароль, введённый пользователем.
        """
        user_info=database.get_data(self.path,text_l)
        if not user_info:
            QMessageBox.information(self, "Failure", "You are not logged in!")
            return
        p_hash = user_info[0][0]
        if self.mode=="on":
            result=hash.check_password(p_hash,text_p)
        else:
            result=without_salt.check_password_w(text_p,p_hash)
        if not result:
            QMessageBox.information(self, "Failure", "Invalid password!")
            return
        if user_info:
            QMessageBox.information(self, "Success", "You have successfully logged in!")
            return


    def signup_button(self,text_l,text_p):
        """
        Обрабатывает регистрацию нового пользователя.

        Проверяет, существует ли пользователь с указанным логином.
        Если нет — в зависимости от режима (с солью или без) хеширует пароль
        и сохраняет запись в базе данных. При успехе выводит сообщение.

        Args:
            text_l (str): Логин пользователя.
            text_p (str): Пароль пользователя.

        """
        user_info=database.get_data(self.path,text_l)
        if user_info:
            QMessageBox.information(self, "Failure", "There is a user with that name.!")
            return
        if self.mode=="on":
            hash_,salt=hash.generate_hash(text_p)
            database.add_user(self.path,text_l,hash_,salt)
        else:
            hash_=without_salt.hash_without_salt(text_p)
            database.add_user(self.path,text_l,hash_,"")
        QMessageBox.information(self, "Success", "You have successfully signed up for the system!")


    def signup(self):
        """
        Метод переключения на окно регистрации
        """
        self.ui.tabWidget.setCurrentIndex(1)
    def signin(self):
        """
        Метод переключения на окно входа
        """
        self.ui.tabWidget.setCurrentIndex(0)

    def design(self):
        """
        Метод применения дизайна

        Скрывает вкладки, устанавливает общую стилизацию через stylehelper,
        а также задаёт тексты-подсказки для всех полей ввода.
        """
        self.ui.tabWidget.tabBar().hide()
        self.setStyleSheet(stylehelper.designAuthentication())
        self.ui.lineEdit_login.setPlaceholderText("Enter your login")
        self.ui.lineEdit_password.setPlaceholderText("Enter your password")
        self.ui.lineEdit_login_2.setPlaceholderText("Enter your login")
        self.ui.lineEdit_password_2.setPlaceholderText("Enter your password")
        self.ui.lineEdit_password_confirm.setPlaceholderText("Confirm your password")

def parsing()-> argparse.Namespace:
    """Получение аргументов командной строки"""
    parser=argparse.ArgumentParser()
    parser.add_argument("--path_db", type=str,default="userdata.db",help="Путь к файлу базы данных")
    parser.add_argument("--salt_mode", type=str,default="on",help="Вкл/выкл использование соли")
    args = parser.parse_args()
    return args.path_db,args.salt_mode

if __name__ == "__main__":
    path,mode=parsing()
    app = QApplication(sys.argv)
    widget = MainWindow(path,mode)
    widget.show()
    sys.exit(app.exec())
