from collections import Counter
from pathlib import Path


INPUT_FILE = "cod23.txt"
FREQUENCY_FILE = "frequency.csv"
DECRYPTED_FILE = "decrypted.txt"
KEY_FILE = "key.txt"


ALPHABET = (
    "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    " "
)


RUSSIAN_FREQUENCIES = {
    " ": 0.128675,
    "О": 0.096456,
    "И": 0.075312,
    "Е": 0.072292,
    "А": 0.064841,
    "Н": 0.061820,
    "Т": 0.061619,
    "С": 0.051953,
    "Р": 0.040677,
    "В": 0.039267,
    "М": 0.029803,
    "Л": 0.029400,
    "Д": 0.026983,
    "Я": 0.026379,
    "К": 0.025977,
    "П": 0.024768,
    "З": 0.015908,
    "Ы": 0.015707,
    "Ь": 0.015103,
    "У": 0.013290,
    "Ч": 0.011679,
    "Ж": 0.010673,
    "Г": 0.009867,
    "Х": 0.008659,
    "Ф": 0.007249,
    "Й": 0.006847,
    "Ю": 0.006847,
    "Б": 0.006645,
    "Ц": 0.005034,
    "Ш": 0.004229,
    "Щ": 0.003625,
    "Э": 0.002416,
    "Ъ": 0.000000,
}


def read_file(file_name: str) -> str:
    """
    Читает содержимое текстового файла.

    :param file_name: имя файла.
    :return: содержимое файла.
    :raises FileNotFoundError: если файл не найден.
    """
    path = Path(file_name)

    with path.open("r", encoding="utf-8") as file:
        return file.read()


def write_file(file_name: str, text: str) -> None:
    """
    Записывает текст в файл.

    :param file_name: имя файла.
    :param text: текст для записи.
    """
    path = Path(file_name)

    with path.open("w", encoding="utf-8") as file:
        file.write(text)


def calculate_frequency(text: str) -> Counter[str]:
    """
    Подсчитывает частоту символов зашифрованного текста.

    Учитываются любые символы, кроме символов новой строки
    и возврата каретки.

    :param text: зашифрованный текст.
    :return: количество появлений каждого символа.
    """
    return Counter(
        char
        for char in text
        if char not in "\n\r"
    )


def get_frequency_order() -> list[str]:
    """
    Возвращает символы русского алфавита в порядке убывания
    их эталонной частоты.

    :return: список символов.
    """
    return sorted(
        ALPHABET,
        key=lambda char: RUSSIAN_FREQUENCIES[char],
        reverse=True,
    )


def get_cipher_frequency_order(
    frequency: Counter[str],
) -> list[str]:
    """
    Возвращает символы шифротекста в порядке убывания
    их фактической частоты.

    :param frequency: частоты символов шифротекста.
    :return: список символов.
    """
    return [
        char
        for char, _ in frequency.most_common()
    ]


def print_frequency_table(frequency: Counter[str]) -> None:
    """
    Выводит таблицу частот для частотного анализа.

    Левая часть таблицы содержит русский алфавит в порядке
    эталонных частот, правая — символы шифротекста в порядке
    фактических частот.

    :param frequency: частоты символов шифротекста.
    """
    russian_order = get_frequency_order()
    cipher_order = get_cipher_frequency_order(frequency)

    total = sum(frequency.values())

    print("\nТаблица частот:")
    print(
        f"{'№':<4}"
        f"{'Символ':<12}"
        f"{'Эталонная частота':<20}"
        f"{'Символ':<12}"
        f"{'Частота текста':<16}"
    )
    print("-" * 64)

    for index, russian_char in enumerate(russian_order, start=1):
        cipher_char = (
            cipher_order[index - 1]
            if index <= len(cipher_order)
            else ""
        )

        cipher_frequency = (
            frequency[cipher_char] / total
            if cipher_char and total > 0
            else 0.0
        )

        russian_display = (
            "ПРОБЕЛ"
            if russian_char == " "
            else russian_char
        )

        cipher_display = (
            "ПРОБЕЛ"
            if cipher_char == " "
            else cipher_char
        )

        print(
            f"{index:<4}"
            f"{russian_display:<12}"
            f"{RUSSIAN_FREQUENCIES[russian_char]:<20.6f}"
            f"{cipher_display:<12}"
            f"{cipher_frequency:<16.6f}"
        )


def create_frequency_file(
    frequency: Counter[str],
) -> str:
    """
    Формирует CSV-таблицу частот.

    :param frequency: частоты символов в тексте.
    :return: содержимое CSV-файла.
    """
    total = sum(frequency.values())
    frequency_order = get_frequency_order()

    lines = [
        "№,Символ,Эталонная частота,"
        "Количество,Частота текста"
    ]

    for index, char in enumerate(
        frequency_order,
        start=1,
    ):
        count = frequency[char]

        if total > 0:
            text_frequency = count / total
        else:
            text_frequency = 0.0

        display_char = "ПРОБЕЛ" if char == " " else char

        lines.append(
            f"{index},{display_char},"
            f"{RUSSIAN_FREQUENCIES[char]:.6f},"
            f"{count},{text_frequency:.6f}"
        )

    return "\n".join(lines)


def decrypt_text(
    text: str,
    key: dict[str, str],
) -> str:
    """
    Дешифрует текст с использованием ключа.

    Ключ хранится в формате:
        исходный символ -> зашифрованный символ.

    Для дешифровки создаётся обратное соответствие:
        зашифрованный символ -> исходный символ.

    :param text: зашифрованный текст.
    :param key: словарь соответствий.
    :return: расшифрованный текст.
    """
    reverse_key = {
        encrypted_char: source_char
        for source_char, encrypted_char in key.items()
    }

    result = []

    for char in text:
        if char in reverse_key:
            result.append(reverse_key[char])
        else:
            result.append(char)

    return "".join(result)


def print_decrypted_text(
    text: str,
    key: dict[str, str],
) -> None:
    """
    Выводит текущую расшифровку текста.

    :param text: зашифрованный текст.
    :param key: текущий ключ.
    """
    decrypted = decrypt_text(text, key)

    print("\n" + "=" * 90)
    print("ТЕКУЩАЯ РАСШИФРОВКА")
    print("=" * 90)
    print(decrypted)
    print("=" * 90)


def print_key(key: dict[str, str]) -> None:
    """
    Выводит текущий ключ подстановки.

    :param key: словарь соответствий.
    """
    print("\n" + "=" * 50)
    print("ТЕКУЩИЙ КЛЮЧ")
    print("=" * 50)

    if not key:
        print("Ключ пока пуст.")
        print("=" * 50)
        return

    print(
        f"{'Зашифрованный':^20}"
        f"{'Исходный':^20}"
    )

    print("-" * 50)

    for encrypted, decrypted in sorted(key.items()):
        encrypted_display = (
            "ПРОБЕЛ"
            if encrypted == " "
            else encrypted
        )

        decrypted_display = (
            "ПРОБЕЛ"
            if decrypted == " "
            else decrypted
        )

        print(
            f"{encrypted_display:^20}"
            f"{decrypted_display:^20}"
        )

    print("=" * 50)


def validate_key_pair(
    key: dict[str, str],
    encrypted_char: str,
    decrypted_char: str,
) -> None:
    """
    Проверяет корректность пары ключа.

    :param key: текущий ключ.
    :param encrypted_char: символ шифротекста.
    :param decrypted_char: символ открытого текста.
    :raises ValueError: если пара некорректна.
    """
    if len(encrypted_char) != 1:
        raise ValueError(
            "Зашифрованный символ должен "
            "состоять из одного символа."
        )

    if len(decrypted_char) != 1:
        raise ValueError(
            "Исходный символ должен "
            "состоять из одного символа."
        )

    encrypted_char = encrypted_char.upper()
    decrypted_char = decrypted_char.upper()

    if encrypted_char not in ALPHABET:
        raise ValueError(
            "Зашифрованный символ отсутствует "
            "в заданном алфавите."
        )

    if (
        encrypted_char in key
        and key[encrypted_char] != decrypted_char
    ):
        raise ValueError(
            f"'{encrypted_char}' уже соответствует "
            f"'{key[encrypted_char]}'."
        )

    for encrypted, decrypted in key.items():
        if (
            decrypted == decrypted_char
            and encrypted != encrypted_char
        ):
            raise ValueError(
                f"Символ '{decrypted_char}' уже используется "
                f"для '{encrypted}'."
            )


def add_key_pair(
    key: dict[str, str],
    encrypted_char: str,
    decrypted_char: str,
) -> None:
    """
    Добавляет пару символов в ключ.

    :param key: текущий ключ.
    :param encrypted_char: символ шифротекста.
    :param decrypted_char: символ открытого текста.
    """
    encrypted_char = encrypted_char.upper()
    decrypted_char = decrypted_char

    validate_key_pair(
        key,
        encrypted_char,
        decrypted_char,
    )

    key[encrypted_char] = decrypted_char


def delete_key_pair(
    key: dict[str, str],
    encrypted_char: str,
) -> None:
    """
    Удаляет соответствие из ключа.

    :param key: текущий ключ.
    :param encrypted_char: символ шифротекста.
    """
    encrypted_char = encrypted_char.upper()

    if encrypted_char == "ПРОБЕЛ":
        encrypted_char = " "

    if encrypted_char in key:
        del key[encrypted_char]

        print(
            f"Соответствие для '{encrypted_char}' удалено."
        )
    else:
        print(
            f"Символ '{encrypted_char}' отсутствует в ключе."
        )


def parse_key_pair(command: str) -> tuple[str, str]:
    """
    Разбирает команду добавления соответствия в ключ.

    Формат команды:
        А -> О
        ПРОБЕЛ -> M
        О -> ПРОБЕЛ

    :param command: введённая команда.
    :return: пара (символ исходного текста, символ шифротекста).
    :raises ValueError: если команда имеет неверный формат.
    """
    if "->" not in command:
        raise ValueError(
            "Используйте формат: А -> О или ПРОБЕЛ -> M."
        )

    left, right = command.split("->", maxsplit=1)

    left = left.strip()
    right = right.strip()

    if left == "ПРОБЕЛ":
        source_char = " "
    elif len(left) == 1:
        source_char = left
    else:
        raise ValueError(
            "Слева должен быть один русский символ "
            "или слово ПРОБЕЛ."
        )

    if right == "ПРОБЕЛ":
        cipher_char = " "
    elif len(right) == 1:
        cipher_char = right
    else:
        raise ValueError(
            "Справа должен быть один символ или слово ПРОБЕЛ."
        )

    return source_char, cipher_char


def print_help() -> None:
    """
    Выводит список доступных команд.
    """
    print(
        """
КОМАНДЫ:

  А -> О
      Добавить соответствие.
      Например: Ф -> О

  delete А
      Удалить соответствие.
      Например: delete Ф

  key
      Показать текущий ключ.

  text
      Показать текущую расшифровку.

  frequency
      Показать таблицу частот.

  help
      Показать справку.

  done
      Завершить подбор и сохранить результат.

  exit
      Выйти без сохранения.
"""
    )


def interactive_decryption(
    encrypted_text: str,
    frequency: Counter[str],
) -> tuple[dict[str, str], bool]:
    """
    Запускает интерактивный подбор ключа.

    :param encrypted_text: зашифрованный текст.
    :param frequency: таблица частот.
    :return: ключ и признак сохранения результата.
    """
    key: dict[str, str] = {}

    print("\n" + "=" * 70)
    print("ИНТЕРАКТИВНЫЙ ПОДБОР КЛЮЧА")
    print("=" * 70)

    print_help()

    while True:
        print_decrypted_text(
            encrypted_text,
            key,
        )

        command = input("\nВведите команду: ").strip()

        if not command:
            continue

        command_lower = command.lower()

        if command_lower == "done":
            return key, True

        if command_lower == "exit":
            return key, False

        if command_lower == "help":
            print_help()
            continue

        if command_lower == "key":
            print_key(key)
            continue

        if command_lower == "text":
            continue

        if command_lower == "frequency":
            print_frequency_table(frequency)
            continue

        if command_lower.startswith("delete "):
            encrypted_char = command[7:].strip()

            try:
                delete_key_pair(
                    key,
                    encrypted_char,
                )
            except ValueError as exc:
                print(f"Ошибка: {exc}")

            continue

        try:
            encrypted_char, decrypted_char = (
                parse_key_pair(command)
            )

            add_key_pair(
                key,
                encrypted_char,
                decrypted_char,
            )

            print(
                f"Добавлено: "
                f"{encrypted_char.upper()} -> "
                f"{decrypted_char}"
            )

        except ValueError as exc:
            print(f"Ошибка: {exc}")


def create_key_file(
    key: dict[str, str],
) -> str:
    """
    Формирует содержимое файла с найденным ключом.

    :param key: найденный ключ.
    :return: текст ключа.
    """
    lines = [
        "Исходный символ -> Зашифрованный символ"
    ]

    for encrypted, decrypted in sorted(key.items()):
        encrypted_display = (
            "ПРОБЕЛ"
            if encrypted == " "
            else encrypted
        )

        decrypted_display = (
            "ПРОБЕЛ"
            if decrypted == " "
            else decrypted
        )

        lines.append(
            f"{encrypted_display} -> {decrypted_display}"
        )

    return "\n".join(lines)


def main() -> None:
    """
    Запускает анализ и интерактивную дешифровку.
    """
    try:
        encrypted_text = read_file(INPUT_FILE)

        frequency = calculate_frequency(
            encrypted_text
        )

        if not frequency:
            raise ValueError(
                "В зашифрованном тексте "
                "отсутствуют символы заданного алфавита."
            )

        print_frequency_table(frequency)

        frequency_text = create_frequency_file(
            frequency
        )

        write_file(
            FREQUENCY_FILE,
            frequency_text,
        )

        key, save_result = interactive_decryption(
            encrypted_text,
            frequency,
        )

        if not save_result:
            print(
                "\nРабота завершена без сохранения."
            )
            return

        decrypted_text = decrypt_text(
            encrypted_text,
            key,
        )

        write_file(
            DECRYPTED_FILE,
            decrypted_text,
        )

        key_text = create_key_file(key)

        write_file(
            KEY_FILE,
            key_text,
        )

        print("\n" + "=" * 70)
        print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ")
        print("=" * 70)
        print(
            f"Таблица частот: {FREQUENCY_FILE}"
        )
        print(
            f"Дешифрованный текст: {DECRYPTED_FILE}"
        )
        print(f"Ключ: {KEY_FILE}")
        print("=" * 70)

    except FileNotFoundError as exc:
        print(f"Ошибка: файл не найден: {exc}")

    except OSError as exc:
        print(f"Ошибка работы с файлом: {exc}")

    except ValueError as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()