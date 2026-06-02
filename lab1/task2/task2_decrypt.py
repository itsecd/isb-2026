def load_cipher_text(path: str) -> str:
    """
    Загружает шифротекст из файла
    Args:
        path (str): путь к файлу
    Returns:
        str: содержимое файла
    Raises:
        FileNotFoundError: если файл отсутствует
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().upper()

    except FileNotFoundError as e:
        print(f"[Ошибка] файл {path} не найден")
        raise e


def replace_symbols(text: str, replace_dict: dict) -> str:
    """
    Выполняет замены символов
    Args:
        text (str): исходный текст
        replace_dict (dict): словарь замен
    Returns:
        str: изменённый текст
    """
    result = ""

    for ch in text:
        result += replace_dict.get(ch, ch)

    return result


def save_decryption_result(text: str,
                           key_data: dict) -> None:
    """
    Сохраняет результат дешифровки и найденный ключ
    Args:
        text (str): расшифрованный текст
        key_data (dict): словарь замен
    """
    try:
        with open(
                "task2_decrypted_text.txt",
                "w",
                encoding="utf-8") as f:
            f.write(text)

        with open(
                "task2_found_key.txt",
                "w",
                encoding="utf-8") as f:

            f.write("Найденный ключ\n")
            f.write("====================\n")

            for old, new in key_data.items():
                if new == " ":
                    f.write(f"{old} -> ПРОБЕЛ\n")
                else:
                    f.write(f"{old} -> {new}\n")

    except IOError as e:
        print("[Ошибка записи файлов]", e)


def main():
    try:
        cipher_text = load_cipher_text("cod18.txt")
    except FileNotFoundError:
        return

    replacements = {}
    current_version = cipher_text

    while True:

        print("\nТЕКУЩИЙ ТЕКСТ:\n")
        print(current_version)

        print("\nТЕКУЩИЕ ЗАМЕНЫ:")

        if replacements:
            for old, new in replacements.items():
                if new == " ":
                    print(f"{old} -> ПРОБЕЛ")
                else:
                    print(f"{old} -> {new}")
        else:
            print("замены отсутствуют")

        old_symbol = input(
            "\nВведите символ для замены (Enter - завершить): "
        ).strip().upper()

        if old_symbol == "":
            break

        if len(old_symbol) != 1:
            print("Введите только один символ")
            continue

        new_symbol = input(
            f'На что заменить "{old_symbol}"? '
        ).strip()

        if new_symbol.lower() == "пробел":
            replacements[old_symbol] = " "
        else:
            replacements[old_symbol] = new_symbol.upper()

        current_version = replace_symbols(
            cipher_text,
            replacements
        )

    if replacements:
        save_decryption_result(
            current_version,
            replacements
        )

        print("\nСозданы файлы:")
        print("- task2_decrypted_text.txt")
        print("- task2_found_key.txt")


if __name__ == "__main__":
    main()
