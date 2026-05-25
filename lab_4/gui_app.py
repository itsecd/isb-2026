import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox, QButtonGroup
from file_open_and_close import load_config, load_user_database, add_user_to_file
from salt_generation import generate_salt
from hash_generation import hash_password
from no_crack import hash_password_no_salt, hash_comparison_no_salt
from hash_comparison import hash_comparison
from picture_demonstration import show_picture

class AppGUI(QWidget):
    def __init__(self, config_path="settings.json"):
        super().__init__()
        self.config_path = config_path
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Password Manager Pro (PyQt5)")
        self.resize(400, 250)
        
        layout = QVBoxLayout()
        
        #Выбор режима
        self.mode_group = QButtonGroup(self)
        self.radio_safe = QRadioButton("Safe Mode (Argon2id + Salt)")
        self.radio_unsafe = QRadioButton("Unsafe Mode (Argon2id NO Salt)")
        self.radio_safe.setChecked(True)
        self.mode_group.addButton(self.radio_safe)
        self.mode_group.addButton(self.radio_unsafe)
        
        layout.addWidget(QLabel("Select system operation mode:"))
        layout.addWidget(self.radio_safe)
        layout.addWidget(self.radio_unsafe)
        
        # Поля ввода
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Username")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.input_user)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.input_password)
        
        # Кнопаськи
        btn_layout = QHBoxLayout()
        self.btn_reg = QPushButton("Register")
        self.btn_login = QPushButton("Login")
        btn_layout.addWidget(self.btn_reg)
        btn_layout.addWidget(self.btn_login)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Клик ивент хэдлеры
        self.btn_reg.clicked.connect(self.handle_registration)
        self.btn_login.clicked.connect(self.handle_login)

    def get_active_db_info(self):
        try:
            config = load_config(self.config_path)
            if self.radio_safe.isChecked():
                db_path = config.get("files", {}).get("data_base", "data_base.json")
                return db_path, True
            else:
                db_path = config.get("files", {}).get("data_base_no_salt", "data_base_no_salt.json")
                return db_path, False
        except Exception as e:
            QMessageBox.critical(self, "Configuration Error", f"Failed to read settings: {e}")
            return "data_base.json", True

    def handle_registration(self):
        username = self.input_user.text().strip()
        password = self.input_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")
            return
            
        try:
            db_path, is_safe = self.get_active_db_info()
            db = load_user_database(db_path)
            
            if username in db:
                QMessageBox.warning(self, "Error", "Username is already taken!")
                return
                
            if is_safe:
                salt = generate_salt()
                pwd_hash = hash_password(password, salt)
                add_user_to_file(db_path, username, pwd_hash, salt)
            else:
                pwd_hash = hash_password_no_salt(password)
                add_user_to_file(db_path, username, pwd_hash, user_salt="none")
                
            QMessageBox.information(self, "Success", "Registration completed successfully!")
            self.input_user.clear()
            self.input_password.clear()
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", f"Error during registration: {e}")

    def handle_login(self):
        username = self.input_user.text().strip()
        password = self.input_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please fill in all fields!")
            return
            
        try:
            db_path, is_safe = self.get_active_db_info()
            db = load_user_database(db_path)
            
            if is_safe:
                success = hash_comparison(db, username, password)
            else:
                success = hash_comparison_no_salt(db, username, password)
                
            if success:
                QMessageBox.information(self, "Access Granted", f"Welcome back, {username}!")
                if is_safe:
                    reply = QMessageBox.question(self, "Hey bud", "Wanna see some pussy?", 
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        show_picture(self.config_path)
            else:
                QMessageBox.warning(self, "Access Denied", "Incorrect username or password.")
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", f"Authentication error: {e}")

def run_gui():
    app = QApplication(sys.argv)
    gui = AppGUI()
    gui.show()
    sys.exit(app.exec_())