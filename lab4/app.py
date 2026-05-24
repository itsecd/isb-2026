import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox, QFrame)
from PyQt5.QtCore import Qt
from backend import Auth

class AuthApp(QWidget):
    def __init__(self, auth_system: Auth):
        super().__init__()
        self.auth = auth_system
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("User Authentication System")
        self.resize(450, 320)
        self.setMinimumSize(400, 300)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)
        
        self.lbl_user = QLabel("Username:")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Enter username")
        
        self.lbl_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText("Enter password")
        
        form_layout.addWidget(self.lbl_user)
        form_layout.addWidget(self.input_user)
        form_layout.addWidget(self.lbl_pass)
        form_layout.addWidget(self.input_pass)
        main_layout.addLayout(form_layout)
        
        default_salt = self.auth.settings.get("use_salt", True)
        self.chk_use_salt = QCheckBox("Use Salt")
        self.chk_use_salt.setChecked(default_salt)
        main_layout.addWidget(self.chk_use_salt)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_reg = QPushButton("Register")
        self.btn_login = QPushButton("Log In")
        
        btn_layout.addWidget(self.btn_reg)
        btn_layout.addWidget(self.btn_login)
        main_layout.addLayout(btn_layout)
        
        self.btn_reg.clicked.connect(self.handle_registration)
        self.btn_login.clicked.connect(self.handle_login)
        
        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F9F9FB;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                color: #2D3748;
            }
            QLabel {
                font-weight: 600;
                color: #4A5568;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3182CE;
            }
            QCheckBox {
                color: #4A5568;
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QPushButton {
                background-color: #3182CE;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2B6CB0;
            }
            QPushButton:pressed {
                background-color: #2C5282;
            }
            QPushButton#Register {
                background-color: #EDF2F7;
                color: #4A5568;
                border: 1px solid #CBD5E0;
            }
            QPushButton#Register:hover {
                background-color: #E2E8F0;
            }
            QPushButton#Register:pressed {
                background-color: #CBD5E0;
            }
        """)
        self.btn_reg.setObjectName("Register")

    def handle_registration(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        
        try:
            if self.chk_use_salt.isChecked():
                self.auth.safe_registration(username, password)
                mode = "with bcrypt"
            else:
                self.auth.unsafe_registration(username, password)
                mode = "without salt"
                
            QMessageBox.information(self, "Success", f"User '{username}' successfully registered {mode}!")
            self.input_pass.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")

    def handle_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        
        try:
            success = self.auth.verify_user(username, password)
            if success:
                QMessageBox.information(self, "Access Granted", "Authorization successful!")
            else:
                QMessageBox.warning(self, "Access Denied", "Invalid username or password!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Authorization error: {str(e)}")

def run_gui(auth_system):
    app = QApplication(sys.argv)
    window = AuthApp(auth_system)
    window.show()
    sys.exit(app.exec_())