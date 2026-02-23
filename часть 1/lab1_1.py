def read_file(file_path: str) -> str:
    """
    Читает файл и возвращает содержимое одной строкой.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print(f"Файл {file_path} успешно загружен")
            return file.read()
    except FileNotFoundError:
        print("Ошибка: файл не найден")
        return ""


def write_file(file_path: str, text: str) -> None:
    """
    Записывает текст в файл.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def load_config(config_path: str) -> int:
    """
    Извлекает сдвиг из файла.
    """
    config_data = read_file(config_path)
    try:
        return int(config_data.strip())
    except ValueError:
        print("Не удалось прочитать сдвиг, используется значение по умолчанию")
        return 1

def string_normal(original_text: str)->str:
    """
    Нормализация строки.
    """
    filtered_chars = ""
    for symb in original_text:
        if symb.isalpha():
            filtered_chars += symb.upper()
    return filtered_chars

def base_coding(filtered_chars:str,shear:int,symbols:list,symbols_size:int)->str:
    """
    Основное кодирование Цезаря.
    """
    result_text = ""
    for symbol in filtered_chars:
        if symbol in symbols:
            curr_index = symbols.index(symbol)
            new_index = (curr_index + shear) % symbols_size
            result_text += symbols[new_index]
    return result_text

def decrypt_process(filtered_enc:str,shear2:int,symbols:list,symbols_size:int)->str:
    """
    Основное декодирование Цезаря.
    """
    decrypted_text = ""
    for symbol in filtered_enc:
        if symbol in symbols:
            curr_index = symbols.index(symbol)
            new_index = (curr_index - shear2) % symbols_size
            decrypted_text += symbols[new_index]
    return decrypted_text

def main():
    """
    Основная функция обработки текста: фильтрация и шифрование.
    """
    start_name = input("Введите имя исходного файла: ").strip()
    result_name = input("Введите имя результирующего файла: ").strip()
    config_name = input("Введите имя файла с параметрами: ").strip()

    if not start_name or not result_name:
        print("Необходимо указать 2 имени")
        return

    original_text = read_file(start_name)
    if not original_text:
        return
    
    shear = load_config(config_name)

    symbols = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    symbols_size = len(symbols)
    filtered_chars=string_normal(original_text)
    result_text=base_coding(filtered_chars,shear,symbols,symbols_size)
    write_file(result_name, result_text)
    print(f"Результат сохранен в файл: {result_name}")

    encrypted_name = input("Введите имя зашифрованного файла: ").strip()
    decrypted_name = input("Введите имя файла для расшифровки: ").strip()
    config_name2 = input("Введите имя файла с параметрами: ").strip()

    if not encrypted_name or not decrypted_name:
        print("Необходимо указать имена файлов")
        return
    encrypted_text = read_file(encrypted_name)
    if not encrypted_text:
        return
    shear2 = load_config(config_name2)

    filtered_enc = string_normal(encrypted_text)

    decrypted_text=decrypt_process(filtered_enc,shear2,symbols,symbols_size)
    write_file(decrypted_name, decrypted_text)
    print(f"Результат расшифровки сохранен в файл: {decrypted_name}")


if __name__ == "__main__":
    main()