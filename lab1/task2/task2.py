from collections import Counter
from constants import TASK2_INPUT, TASK2_OUTPUT, TASK2_FREQ
from cod13_key import KEY


def load_text(filename: str) -> str:
    """
    Загружает текст из файла.

    :param filename: имя входного файла
    :return: содержимое файла
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        raise
    except IOError as e:
        print(f"Ошибка чтения файла '{filename}': {e}")
        raise


def save_text(filename: str, data: str) -> None:
    """
    Сохраняет текст в файл.

    :param filename: имя выходного файла
    :param data: данные для записи
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
    except IOError as e:
        print(f"Ошибка записи в файл '{filename}': {e}")
        raise


def calculate_frequencies(text: str) -> str:
    """
    Вычисляет относительные частоты символов.

    :param text: входной текст
    :return: строка с отсортированным словарем частот
    """
    if not text:
        return "{}"

    total = len(text)
    counter = Counter(text)
    freq_dict = {char: count / total for char, count in counter.items()}
    sorted_freq = dict(sorted(freq_dict.items(),
                              key=lambda x: x[1],
                              reverse=True))
    return str(sorted_freq)


def decrypt(text: str, key: dict) -> str:
    """
    Дешифрует текст с использованием словаря подстановки.

    :param text: зашифрованный текст
    :param key: словарь соответствий
    :return: расшифрованный текст
    """
    return "".join(key.get(char, char) for char in text)


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        text = load_text(TASK2_INPUT)
        frequencies = calculate_frequencies(text)
        save_text(TASK2_FREQ, frequencies)

        decrypted_text = decrypt(text, KEY)
        save_text(TASK2_OUTPUT, decrypted_text)

        print("Готово.")
    except Exception as e:
        print(f"Ошибка выполнения: {e}")


if __name__ == "__main__":
    main()