import string
import sys
import argparse
import re
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
)


class MainWindow(QMainWindow):
    def __init__(self, input_file=None, key_file=None, output_file=None):
        super().__init__()
        self.input_file = input_file
        self.key_file = key_file
        self.output_file = output_file
        self.RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя. ,"
        self.setWindowTitle("Шифр Полибия")
        self.resize(400, 350)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Ключ"))
        self.key_input = QLineEdit()
        layout.addWidget(self.key_input)

        layout.addWidget(QLabel("Текст"))
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        layout.addWidget(QLabel("Результат:"))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        btn = QPushButton("Зашифровать")
        btn.setFixedSize(100, 50)
        btn.clicked.connect(self.encrypt)
        layout.addWidget(btn)

        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.setFixedSize(100, 50)
        decrypt_btn.clicked.connect(self.decrypt)
        layout.addWidget(decrypt_btn)

        central.setLayout(layout)

        if self.input_file:
            content = read_file(self.input_file)
            if content is not None:
                self.text_input.setPlainText(content)

        if self.key_file:
            input_key = read_file(self.key_file)
            if input_key is not None:
                self.key_input.setText(input_key)

    def encrypt(self):
        key = self.key_input.text().strip()
        text = self.text_input.toPlainText().strip()
        if not key or not text:
            error_msg = "Ошибка: отсутствует ключ или текст"
            self.result_output.setPlainText(error_msg)
            return
        key_chars = create_key(key)
        full_alphabet = create_full_alphabet(self.RUSSIAN_ALPHABET, key_chars)
        char_to_codes = create_polybius(full_alphabet)
        result = polybius_cipher(text, char_to_codes)

        self.result_output.setPlainText(result)
        if self.output_file:
            write_result_to_file(result, self.output_file)

    def decrypt(self):
        key = self.key_input.text().strip()
        text = self.text_input.toPlainText().strip()
        if not key or not text:
            error_msg = "Ошибка: отсутствует ключ или текст"
            self.result_output.setPlainText(error_msg)
            return
        key_chars = create_key(key)
        full_alphabet = create_full_alphabet(self.RUSSIAN_ALPHABET, key_chars)
        char_to_codes = create_polybius(full_alphabet)
        result = decryption(char_to_codes, text)

        self.result_output.setPlainText(result)


def create_key(key):
    key_chars = []
    seen = set()
    key = key.lower()
    for char in key:
        if char not in seen:
            key_chars.append(char)
            seen.add(char)
    return key_chars


def create_full_alphabet(alphabet, key_chars):
    alphabet = alphabet.lower()
    remaining = [char for char in alphabet if char not in key_chars]
    return key_chars + remaining


def create_polybius(full_over):
    square = [full_over[i : i + 6] for i in range(0, 36, 6)]
    char_to_codes = {}
    for i in range(6):
        for j in range(6):
            char = square[i][j]
            char_to_codes[char] = str(i + 1) + str(j + 1)
    return char_to_codes


def polybius_cipher(text, char_to_codes):
    text = text.lower()
    encoded = ""
    for char in text:
        if char in char_to_codes:
            encoded += char_to_codes[char]
    return encoded.strip()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", help="Путь к файлу для обработки")
    parser.add_argument("output_file", help="Путь к файлу для записи результата")
    parser.add_argument("key", help="Ключ шифрования")
    return parser.parse_args()


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        return None
    except Exception as e:
        print("Ошибка при чтении файла:", e)
        return None


def write_result_to_file(result, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(result)
    except Exception as e:
        print("Ошибка при записи результата в файл:", e)


def decryption(char_to_coders, encoded):
    decoded = ""
    coders_to_char = {}
    for ch in char_to_coders:
        code = char_to_coders[ch]
        coders_to_char[code] = ch
    encoded_strip = re.findall(r"\d\d", encoded)
    for code in encoded_strip:
        if code in coders_to_char:
            decoded += coders_to_char[code]
    return decoded


if __name__ == "__main__":
    args = parse_arguments()
    app = QApplication(sys.argv)
    window = MainWindow(
        input_file=args.input_file, key_file=args.key, output_file=args.output_file
    )
    window.show()
    sys.exit(app.exec())
