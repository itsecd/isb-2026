'''Модуль главного окна приложения для шифрования и дешифрования текста.

Предоставляет графический интерфейс для выбора алгоритма шифрования,
ввода сообщения и ключа, а также выполнения операций шифрования/дешифрования.
Поддерживает русский и английский алфавиты, шифр подстановки и Виженера.
'''
import sys
from PyQt5 import QtWidgets
from des import *
from SubstitutionCipher import keyIsValidSub, decryptMessageSubstitution, encryptMessageSubstitution
from VigenerChipher import encryptMessageViginer, decryptMessageViginer, keyIsValidVig

RUSSIAN_ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class MyWin(QtWidgets.QMainWindow):
    """
    Главное окно приложения.
    
    Предоставляет пользовательский интерфейс для выбора языка, типа шифра,
    операции (шифрование/дешифрование), ввода сообщения и ключа.
    Обрабатывает все пользовательские действия и взаимодействует с модулями шифрования.
    
    Attributes:
        ui (Ui_encryption): Сгенерированный класс интерфейса из des.py
    """
    def __init__(self, parent=None):
        """
        Инициализирует главное окно и настраивает пользовательский интерфейс.
        """

        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Ui_encryption()
        self.ui.setupUi(self)
        # Подключаем сигналы
        self.ui.execute.clicked.connect(self.processing_message)
        self.ui.openFile.triggered.connect(self.open_message)
        self.ui.openKey.triggered.connect(self.open_key)
        self.ui.saveMessage.triggered.connect(self.save_message)
        self.ui.saveEncryptMes.triggered.connect(self.save_Encrypt_message)
        self.ui.saveKey.triggered.connect(self.save_key)

    def processing_message(self):
        """
        Основной метод обработки сообщения.
        
        Выполняет полный цикл обработки:
        1. Проверяет заполненность полей
        2. Определяет выбранный алфавит
        3. Проверяет валидность ключа
        4. Выполняет шифрование/дешифрование
        5. Выводит результат
        """
        #Проверяем заполненость полей сообщения и ключа
        if not self.check_fields():
           return 
        # Получаем алфавит
        alphabet = self._get_alphabet()
        
        # Получаем ключ и проверяем его валидность
        key = self.ui.key.toPlainText()
        if not self.keyIsValid(key, alphabet):
            return
        
        # Выполняем шифрование/дешифрование
        result = self._process_cipher(key, alphabet)
        
        # Выводим результат
        if result:
            self.ui.return_message.setPlainText(result)
    
    def check_fields(self) -> bool:
        """       
        Проверяет поля "Сообщение" и "Ключ" на наличие текста.
        В случае отсутствия текста показывает предупреждение пользовател
        """
        message_text = self.ui.message.toPlainText().strip()
        key_text = self.ui.key.toPlainText().strip()

        empty_fields = []

        #Если пустое поле сообщения
        if not message_text:
            empty_fields.append("Сообщение")
        #Если пустое поля ключа
        if not key_text:
            empty_fields.append("Ключ")

        if empty_fields:
            error_message = f"Заполните следующие поля:\n- " + "\n- ".join(empty_fields)
            QtWidgets.QMessageBox.warning(self, 'ОШИБКА', error_message)
            return False
        return True
    
    def _get_alphabet(self) ->str:
        """Возвращает выбранный алфавит"""
        if self.ui.language.currentIndex() == 0:
            return RUSSIAN_ALPHABET
        elif self.ui.language.currentIndex() == 1:
            return ENGLISH_ALPHABET        
   
    def keyIsValid(self, key, alphabet)->bool:
        """
        Проверяет валидность ключа для выбранного типа шифра.
        Для шифра подстановки проверяет уникальность символов и длину ключа.
        Для шифра Виженера проверяет, что все символы ключа входят в алфавит.
        key: Ключ для проверки
        alphabet: Используемый алфавит
        """
        cipher_type = self.ui.name_chipher.currentIndex()

        if cipher_type == 0:  # шифр подстановкой
            is_valid = keyIsValidSub(key, alphabet)
            if not is_valid:
                empty_fields = []
                if len(key)!=len(set(key)):
                  empty_fields.append("В ключе есть повторяющиеся символы")
                if len(set(key)) != len(alphabet):
                    empty_fields.append(f"Недостаточно букв для алфавита({len(set(key))})")
                if empty_fields:
                    error_message = f"Ошибка формата ключа:\n- " + "\n- ".join(empty_fields)
                    QtWidgets.QMessageBox.warning(self, 'ОШИБКА', error_message)

        elif cipher_type == 1:  # шифр Виженера
            is_valid = keyIsValidVig(key, alphabet)
            if not is_valid:
                QtWidgets.QMessageBox.warning(self, 'ОШИБКА', 'Символы ключа не соответствуют алфавиту')
        return is_valid
    
    def _process_cipher(self, key, alphabet):
        """Выполняет шифрование или дешифрование в зависимости от выбора
        key: Ключ шифрования
        alphabet: Используемый алфавит"""

        procedure = self.ui.procedure.currentIndex()
        cipher_type = self.ui.name_chipher.currentIndex()
        message = self.ui.message.toPlainText()

        # Словарь с функциями для разных комбинаций
        operations = {
            (0, 0): encryptMessageSubstitution,  # шифр + подстановка
            (0, 1): encryptMessageViginer,       # шифр + Виженер
            (1, 0): decryptMessageSubstitution,   # дешифр + подстановка
            (1, 1): decryptMessageViginer         # дешифр + Виженер
        }

        operation = operations.get((procedure, cipher_type))
        if operation:
            return operation(key, alphabet, message)  
    
    def open_message(self):
        """Открывает файл и загружает его содержимое в поле сообщения"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Открыть редактируемый файл", 
            '', 
            'Document *.txt'
        )

        if file_path:  # Если файл выбран
            with open(file_path, "r", encoding='utf-8') as file:
                message = file.read()
            self.ui.message.setPlainText(message)
        else:
            QtWidgets.QMessageBox.information(self, 'information', 'Файл не выбран' )

    def open_key(self):
        """Открывает файл и загружает его содержимое в поле ключа"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Открыть редактируемый файл", 
            '', 
            'Document *.txt'
        )

        if file_path:  
            with open(file_path, "r", encoding='utf-8') as file:
                message = file.read()
            self.ui.key.setPlainText(message)
        else:
            QtWidgets.QMessageBox.information(self, 'information', 'Файл не выбран' )
    
    def save_message(self):
        """Сохраняет содержимое поля сообщения в файл"""

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Сохранить редактируемый файл", 
            "", 
            "Текстовые файлы (*.txt)"
        )
        if file_path:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(self.ui.message.toPlainText())
    
    def save_Encrypt_message(self):
        """Сохраняет результат шифрования/дешифрования в файл"""

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Сохранить результируюий файл", 
            "", 
            "Текстовые файлы (*.txt)"
        )
        if file_path:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(self.ui.return_message.toPlainText())
    
    def save_key(self):
        """ Сохраняет содержимое поля ключа в файл"""

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Сохранить редактируемый файл", 
            "", 
            "Текстовые файлы (*.txt)"
        )
        if file_path:
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(self.ui.key.toPlainText())   

if __name__ == '__main__':
    """Точка входа в приложение"""
    
    app = QtWidgets.QApplication(sys.argv)
    mayapp = MyWin()
    mayapp.show()
    sys.exit(app.exec_())
