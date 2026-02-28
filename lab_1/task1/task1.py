import pandas as pd


def read_text(filename: str) -> str:
    """
    Чтение текста из файла.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Файл не найден")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


def write_text(filename: str, text: str) -> None:
    """
    Запись текста в файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(e)
        exit(1)


def read_key(filename: str) -> tuple[str, str]:
    """
    Чтение ключа из key1.txt через pandas.
    """
    try:
        df = pd.read_csv(filename, header=None)

        if len(df) < 2:
            print("В файле ключа должно быть две строки")
            exit(1)

        alphabet = df.iloc[0, 0].strip()
        reversed_alphabet = df.iloc[1, 0].strip()

        if len(alphabet) != len(reversed_alphabet):
            print("Строки ключа разной длины")
            exit(1)

        return alphabet, reversed_alphabet

    except FileNotFoundError:
        print("Файл ключа не найден")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


def build_map(source: str, target: str) -> dict[str, str]:
    """
    Создание словаря соответствий символов.
    """
    return dict(zip(source, target))


def transform(text: str, mapping: dict[str, str]) -> str:
    """
    Универсальная функция для шифрования и дешифрования.
    """
    result = ""
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result


def main() -> None:
    """Основная функция: чтение ключа, шифрование и дешифрование."""
    alphabet, reversed_alphabet = read_key("key1.txt")

    enc_map = build_map(alphabet, reversed_alphabet)
    dec_map = build_map(reversed_alphabet, alphabet)

    text = read_text("original1.txt")

    cipher_text = transform(text, enc_map)
    write_text("cipher1.txt", cipher_text)

    decoded_text = transform(cipher_text, dec_map)
    write_text("decoded1.txt", decoded_text)

    print("Готово.")
    print("Созданы файлы:")
    print("cipher1.txt")
    print("decoded1.txt")


if __name__ == "__main__":
    main()
