def read_cipher_file(path: str) -> str:
    """
    Загружает зашифрованный текст из файла
    Args:
        path (str): путь к файлу
    Returns:
        str: текст в верхнем регистре
    Raises:
        FileNotFoundError: если файл не найден
        UnicodeDecodeError: если проблема с кодировкой
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().upper()

    except FileNotFoundError as e:
        print(f"[Ошибка] файл не найден: {path}")
        raise e

    except UnicodeDecodeError as e:
        print(f"[Ошибка] проблема кодировки файла: {path}")
        raise e


def frequency_analysis(text: str) -> list:
    """
    Считает частоты символов в тексте
    Args:
        text (str): входной текст
    Returns:
        list: список (символ, количество, процент)
    """
    total = len(text)
    counter = {}

    for ch in text:
        counter[ch] = counter.get(ch, 0) + 1

    result = []

    for ch, count in counter.items():
        percent = (count / total) * 100
        result.append((ch, count, percent))

    return sorted(result, key=lambda x: x[1], reverse=True)


def print_frequency_table(freq_data: list) -> None:
    """
    Выводит таблицу частот символов
    Args:
        freq_data (list): данные частот
    """
    print("\nАНАЛИЗ ЧАСТОТ:\n")
    print("Символ | Кол-во | %")
    print("---------------------")

    for ch, count, percent in freq_data[:15]:

        if ch == " ":
            display = "ПРОБЕЛ"
        elif ch == "\n":
            display = "\\n"
        else:
            display = ch

        print(f"{display:7} | {count:6} | {percent:6.2f}")


def save_frequency_file(
        freq_data: list,
        filename: str = "task2_frequency_table.txt") -> None:
    """
    Сохраняет результаты частотного анализа
    Args:
        freq_data (list): список частот
        filename (str): имя файла
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:

            f.write("Символ | Кол-во | Частота (%)\n")
            f.write("------------------------------\n")

            for ch, count, percent in freq_data:

                if ch == " ":
                    display = "ПРОБЕЛ"
                elif ch == "\n":
                    display = "\\n"
                else:
                    display = ch

                f.write(
                    f"{display:7} | {count:6} | {percent:6.2f}\n"
                )

    except IOError as e:
        print("[Ошибка записи файла]", e)


def main():
    try:
        cipher_text = read_cipher_file("cod18.txt")

    except (FileNotFoundError, UnicodeDecodeError):
        return

    frequencies = frequency_analysis(cipher_text)

    print_frequency_table(frequencies)

    save_frequency_file(frequencies)

    print("\nГотово:")
    print("- частотный анализ выполнен")
    print("- результат сохранён в task2_frequency_table.txt")


if __name__ == "__main__":
    main()
