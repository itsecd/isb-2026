import math


def read_file(filename):
    """Чтение текстового файла"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, text):
    """Запись текста в файл"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def clean_text(text):
    """Удаление пробельных символов из текста"""
    return "".join(text.split())


def encrypt(text, key):
    """Шифрование текста методом столбцовой перестановки"""
    text = clean_text(text)

    columns = len(key)
    rows = math.ceil(len(text) / columns)

    text += "Х" * (rows * columns - len(text))

    matrix = [
        list(text[i * columns:(i + 1) * columns])
        for i in range(rows)
    ]

    key_order = sorted(
        [(symbol, index) for index, symbol in enumerate(key)]
    )

    encrypted_text = ""

    for _, column_index in key_order:
        for row in matrix:
            encrypted_text += row[column_index]

    return encrypted_text


if __name__ == "__main__":
    text = read_file("input.txt")
    key = read_file("key.txt").strip()

    encrypted = encrypt(text, key)
    write_file("encrypted.txt", encrypted)

    print("Шифрование завершено")