# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(361, 400)
        MainWindow.setMinimumSize(QSize(300, 400))
        MainWindow.setMaximumSize(QSize(361, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, 0, 20, 0)
        self.verticalLayout_window = QVBoxLayout()
        self.verticalLayout_window.setSpacing(0)
        self.verticalLayout_window.setObjectName(u"verticalLayout_window")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer)

        self.label_head = QLabel(self.tab)
        self.label_head.setObjectName(u"label_head")
        self.label_head.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_window.addWidget(self.label_head)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer_3)

        self.verticalLayout_l = QVBoxLayout()
        self.verticalLayout_l.setSpacing(0)
        self.verticalLayout_l.setObjectName(u"verticalLayout_l")
        self.label_login = QLabel(self.tab)
        self.label_login.setObjectName(u"label_login")
        self.label_login.setMinimumSize(QSize(0, 20))
        self.label_login.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_l.addWidget(self.label_login)

        self.lineEdit_login = QLineEdit(self.tab)
        self.lineEdit_login.setObjectName(u"lineEdit_login")
        self.lineEdit_login.setMinimumSize(QSize(0, 40))
        self.lineEdit_login.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_l.addWidget(self.lineEdit_login)


        self.verticalLayout_window.addLayout(self.verticalLayout_l)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer_6)

        self.verticalLayout_p = QVBoxLayout()
        self.verticalLayout_p.setSpacing(0)
        self.verticalLayout_p.setObjectName(u"verticalLayout_p")
        self.label_password = QLabel(self.tab)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setMinimumSize(QSize(0, 20))
        self.label_password.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_p.addWidget(self.label_password)

        self.lineEdit_password = QLineEdit(self.tab)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 40))
        self.lineEdit_password.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_p.addWidget(self.lineEdit_password)


        self.verticalLayout_window.addLayout(self.verticalLayout_p)

        self.verticalSpacer_4 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer_4)

        self.pushbutton_login = QPushButton(self.tab)
        self.pushbutton_login.setObjectName(u"pushbutton_login")
        self.pushbutton_login.setMinimumSize(QSize(0, 40))
        self.pushbutton_login.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_window.addWidget(self.pushbutton_login)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer_5)

        self.horizontalLayout_t = QHBoxLayout()
        self.horizontalLayout_t.setSpacing(0)
        self.horizontalLayout_t.setObjectName(u"horizontalLayout_t")
        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_t.addItem(self.horizontalSpacer)

        self.label_text = QLabel(self.tab)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMinimumSize(QSize(0, 20))
        self.label_text.setMaximumSize(QSize(16777215, 20))
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_t.addWidget(self.label_text)

        self.pushbutton_signup_1 = QPushButton(self.tab)
        self.pushbutton_signup_1.setObjectName(u"pushbutton_signup_1")
        self.pushbutton_signup_1.setMinimumSize(QSize(0, 21))
        self.pushbutton_signup_1.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_t.addWidget(self.pushbutton_signup_1)

        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_t.addItem(self.horizontalSpacer_2)


        self.verticalLayout_window.addLayout(self.horizontalLayout_t)

        self.verticalSpacer_7 = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window.addItem(self.verticalSpacer_7)


        self.verticalLayout_4.addLayout(self.verticalLayout_window)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout = QVBoxLayout(self.tab_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 0, 20, 0)
        self.verticalLayout_window_2 = QVBoxLayout()
        self.verticalLayout_window_2.setSpacing(0)
        self.verticalLayout_window_2.setObjectName(u"verticalLayout_window_2")
        self.label_head_2 = QLabel(self.tab_2)
        self.label_head_2.setObjectName(u"label_head_2")
        self.label_head_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_window_2.addWidget(self.label_head_2)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window_2.addItem(self.verticalSpacer_8)

        self.verticalLayout_l_2 = QVBoxLayout()
        self.verticalLayout_l_2.setSpacing(0)
        self.verticalLayout_l_2.setObjectName(u"verticalLayout_l_2")
        self.label_login_2 = QLabel(self.tab_2)
        self.label_login_2.setObjectName(u"label_login_2")
        self.label_login_2.setMinimumSize(QSize(0, 20))
        self.label_login_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_l_2.addWidget(self.label_login_2)

        self.lineEdit_login_2 = QLineEdit(self.tab_2)
        self.lineEdit_login_2.setObjectName(u"lineEdit_login_2")
        self.lineEdit_login_2.setMinimumSize(QSize(0, 40))
        self.lineEdit_login_2.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_l_2.addWidget(self.lineEdit_login_2)


        self.verticalLayout_window_2.addLayout(self.verticalLayout_l_2)

        self.verticalLayout_p_2 = QVBoxLayout()
        self.verticalLayout_p_2.setSpacing(0)
        self.verticalLayout_p_2.setObjectName(u"verticalLayout_p_2")
        self.label_password_2 = QLabel(self.tab_2)
        self.label_password_2.setObjectName(u"label_password_2")
        self.label_password_2.setMinimumSize(QSize(0, 20))
        self.label_password_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_p_2.addWidget(self.label_password_2)


        self.verticalLayout_window_2.addLayout(self.verticalLayout_p_2)

        self.lineEdit_password_2 = QLineEdit(self.tab_2)
        self.lineEdit_password_2.setObjectName(u"lineEdit_password_2")
        self.lineEdit_password_2.setMinimumSize(QSize(0, 40))
        self.lineEdit_password_2.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_window_2.addWidget(self.lineEdit_password_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_password_confirm = QLabel(self.tab_2)
        self.label_password_confirm.setObjectName(u"label_password_confirm")
        self.label_password_confirm.setMinimumSize(QSize(0, 20))
        self.label_password_confirm.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.label_password_confirm)

        self.lineEdit_password_confirm = QLineEdit(self.tab_2)
        self.lineEdit_password_confirm.setObjectName(u"lineEdit_password_confirm")
        self.lineEdit_password_confirm.setMinimumSize(QSize(0, 40))
        self.lineEdit_password_confirm.setMaximumSize(QSize(16777215, 40))
        self.lineEdit_password_confirm.setSizeIncrement(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.lineEdit_password_confirm)


        self.verticalLayout_window_2.addLayout(self.verticalLayout_2)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window_2.addItem(self.verticalSpacer_10)

        self.pushbutton_signup = QPushButton(self.tab_2)
        self.pushbutton_signup.setObjectName(u"pushbutton_signup")
        self.pushbutton_signup.setMinimumSize(QSize(0, 40))
        self.pushbutton_signup.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout_window_2.addWidget(self.pushbutton_signup)

        self.verticalSpacer_11 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window_2.addItem(self.verticalSpacer_11)

        self.horizontalLayout_t_2 = QHBoxLayout()
        self.horizontalLayout_t_2.setSpacing(0)
        self.horizontalLayout_t_2.setObjectName(u"horizontalLayout_t_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_t_2.addItem(self.horizontalSpacer_3)

        self.label_text_2 = QLabel(self.tab_2)
        self.label_text_2.setObjectName(u"label_text_2")
        self.label_text_2.setMinimumSize(QSize(0, 20))
        self.label_text_2.setMaximumSize(QSize(16777215, 20))
        self.label_text_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_t_2.addWidget(self.label_text_2)

        self.pushbutton_signin = QPushButton(self.tab_2)
        self.pushbutton_signin.setObjectName(u"pushbutton_signin")
        self.pushbutton_signin.setMinimumSize(QSize(0, 21))
        self.pushbutton_signin.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_t_2.addWidget(self.pushbutton_signin)

        self.horizontalSpacer_4 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_t_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_window_2.addLayout(self.horizontalLayout_t_2)

        self.verticalSpacer_12 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_window_2.addItem(self.verticalSpacer_12)


        self.verticalLayout.addLayout(self.verticalLayout_window_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Application", None))
        self.label_head.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label_login.setText(QCoreApplication.translate("MainWindow", u"Login:", None))
        self.label_password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.pushbutton_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label_text.setText(QCoreApplication.translate("MainWindow", u"Dont`t have an account?", None))
        self.pushbutton_signup_1.setText(QCoreApplication.translate("MainWindow", u"Sign up here", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.label_head_2.setText(QCoreApplication.translate("MainWindow", u"Signup", None))
        self.label_login_2.setText(QCoreApplication.translate("MainWindow", u"Login:", None))
        self.label_password_2.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.label_password_confirm.setText(QCoreApplication.translate("MainWindow", u"Confirm password:", None))
        self.pushbutton_signup.setText(QCoreApplication.translate("MainWindow", u"Signup", None))
        self.label_text_2.setText(QCoreApplication.translate("MainWindow", u"Have an account?", None))
        self.pushbutton_signin.setText(QCoreApplication.translate("MainWindow", u"Sign in here", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

