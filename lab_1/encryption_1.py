
""" Реализация шифрования и дешифрования произвольного текста методом квадрата Полибия. """

from constants import (
    ALPHABET,
    SQUARE_SIZE,
    KEY_TEXT_FRST,
    CLEAN_TEXT_FRST,
    TEXT_FRST,
    RESULT_FRST_DECRY,
    RESULT_FRST_ENCRY,
)


def build_square_table(alphabet, square_size):

    """ Построение квадрата Полибия по используемому алфавиту с разделением по длине строки. """

    square_table = []

    for i in range(0, len(ALPHABET), SQUARE_SIZE):
        square_table.append(ALPHABET[i:i + SQUARE_SIZE])

    return square_table


def encrypt(text, square_table):

    """ Шифрование текста с заменой каждой буквы на ее соотвествующие координаты в квадрате Полибия. """

    result = ""

    for letter in text:
        for row in range(len(square_table)):
            if letter in square_table[row]:
                column = square_table[row].index(letter)
                result += str(row + 1) + str(column + 1) + " "

    return result


def decrypt(cipher_text, square_table):

    """ Дешифрование исходного текста по координатам из квадрата Полибия. """

    result = ""

    numbers = cipher_text.split()

    for pair in numbers:
        row = int(pair[0]) - 1
        column = int(pair[1]) - 1
        result += square_table[row][column]

    return result


def read_file(filename):

    """ Чтение содержимого файла. """

    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, text):

    """ Запись переданного текста в файл. """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def save_key(square, filename):

    """ Сохранение ключа замены в файл. """

    with open(filename, "w", encoding="utf-8") as file:
        for row in square:
            file.write(row + "\n")


def clean_text(text, alphabet):

    """ Проверка исходного текста на содержание в нем символов/букв, не содержащихся в заданном алфавите. """

    result = ""

    for char in text.upper():
        if char in ALPHABET:
            result += char

    return result


def main():

    """ Главная функция. """

    square = build_square_table(ALPHABET, SQUARE_SIZE)

    text = read_file(TEXT_FRST)

    text = clean_text(text, ALPHABET)

    write_file(CLEAN_TEXT_FRST, text)

    cipher = encrypt(text, square)

    write_file(RESULT_FRST_ENCRY, cipher)

    decrypted = decrypt(cipher, square)

    write_file(RESULT_FRST_DECRY, decrypted)

    save_key(square, KEY_TEXT_FRST)

    print("Зашифрование и дешифрование текста выполнено.")


if __name__ == "__main__":
    main()