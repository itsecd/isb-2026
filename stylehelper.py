# This Python file uses the following encoding: utf-8


class stylehelper:
    @staticmethod
    def designAuthentication():
        return """
                QWidget{
                background-color:white;
                color:black;
                font-weight:bold;
                }
                QPushButton#pushbutton_login, QPushButton#pushbutton_signup{
                background-color:#0000ff;
                border-radius:20px;
                color:white;
                font:14px;
                font-weight:bold;
                }
                QPushButton#pushbutton_login::pressed, QPushButton#pushbutton_signup::pressed{
                background-color:#0000cc;
                }
                QPushButton#pushbutton_signup_1, QPushButton#pushbutton_signin{
                background-color:white;
                color:#6666ff;
                }
                QPushButton#pushbutton_signup_1:hover, QPushButton#pushbutton_signin:hover{
                background-color:white;
                color: #3333ff;
                }
                QLineEdit{
                border:1px solid #e0e0e0;
                border-radius:5px;
                }
                QLabel#label_head,QLabel#label_head_2{
                font:20px;
                font-weight:bold;
                }
                QLineEdit:focus{
                border:2px solid #2a2a2a;
                }
               """


