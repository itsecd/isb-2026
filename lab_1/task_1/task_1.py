import math


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
    text = "пример текста"
    key = "ключ"
    print(encrypt(text, key))