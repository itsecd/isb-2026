"""
Лабораторная работа 1, задание 1: Омофонический шифр
Программа шифрует текст из файла с использованием омофонической замены
"""

print("Лабораторная1,задание 1: омофонический шифр")

# Путь до папки staff_task1
staff_path = "staff_task1/"


def load_text_file(filename: str) -> str:
    """
    Загружает текстовый файл и возвращает его содержимое.

    Args:
        filename (str): Имя файла для загрузки

    Returns:
        str: Содержимое файла
    """
    with open(staff_path + filename, 'r', encoding='utf-8') as file:
        return file.read()


def load_cipher_table(filename: str) -> dict:
    """
    Загружает таблицу шифрования из файла.

    Args:
        filename (str): Имя файла с таблицей шифрования

    Returns:
        dict: Словарь с таблицей шифрования
    """
    with open(staff_path + filename, 'r', encoding='utf-8') as table_file:
        table_str = table_file.read()
        return eval(table_str)


def save_encrypted_text(filename: str, encrypted_text: str) -> None:
    """
    Сохраняет зашифрованный текст в файл.

    Args:
        filename (str): Имя файла для сохранения
        encrypted_text (str): Зашифрованный текст
    """
    with open(staff_path + filename, 'w', encoding='utf-8') as output_file:
        output_file.write(encrypted_text)


def encrypt_text(original_text: str, cipher_table: dict) -> str:
    """
    Шифрует текст с использованием омофонической таблицы.
    Args:
        original_text (str): Исходный текст для шифрования
        cipher_table (dict): Таблица омофонической замены

    Returns:
        str: Зашифрованный текст
    """
    code = ""
    for char in original_text:
        lower_char = char.lower()
        if lower_char in cipher_table:
            index = cipher_table[lower_char][3]
            code += cipher_table[lower_char][index]
            cipher_table[lower_char][3] = (index + 1) % 3
        else:
            code += char
    return code


def main():
    """Основная функция программы."""
    # Загрузка исходного текста
    text = load_text_file('lab1_task1.txt')
    original = list(text)

    # Загрузка таблицы шифрования
    table = load_cipher_table('task1_key.txt')

    # Шифрование текста
    code = encrypt_text(original, table)

    # Сохранение результата
    save_encrypted_text('lab1_task1.5.txt', code)

    print("\n=== Зашифрованное сообщение сохранено в файл 'lab1_task1.5.txt' в папке staff_task1 ===")


if __name__ == "__main__":
    main()
