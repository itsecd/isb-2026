import work_file1


ALPHABETS = "АБВГДЕЖЗИЙКЛМОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
def letter_trans() -> dict:
    """
    Создаёт таблицу шифрования (ключ шифра) по методу сдвига Цезаря.
    Каждая буква русского алфавита сдвигается вправо на 4 позиции.

    """
    dict1 = {}
    for letter in ALPHABETS:
        pos = ALPHABETS.find(letter)
        new_pos = (pos + 4) % len(ALPHABETS)
        dict1[letter] = ALPHABETS[new_pos]
    work_file1.write_file("encryption_key", dict1)
    return dict1


def encryption(file_name: str) -> None:
    """
    Выполняет шифрование текста с использованием таблицы замены.
    """
    text = work_file1.read_file_txt("original_text").upper()
    dict1 = letter_trans()
    text = text.translate(str.maketrans(dict1))
    work_file1.write_file_txt(file_name, text)

def decryption(file_name: str, key: dict) -> None:
    """
    Расшифровка зашифрованного текста
    """

    text = work_file1.read_file_txt("encrypted_text")
    text = text.translate(str.maketrans(key))
    work_file1.write_file_txt(file_name, text)

def main() -> None:
    """Основная функция"""
    encryption("encrypted_text")

    key = work_file1.read_file("decryption_key")
    decryption("decrypted_text", key)

if __name__ == "__main__":
    main()