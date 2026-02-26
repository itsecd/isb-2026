from const import *

def encryption(text, key):
    """Шифрование текста"""
    result = []
    k = -1
    key_len = len(key)

    for char in text:
        if char not in ALPHABET:
            result.append(char)
            continue

        k += 1
        if k == key_len:
            k = 0

        num = ALPHABET[char] + ALPHABET[key[k]]

        if num > len(ALPHABET):
            num -= len(ALPHABET)

        result.append(ALPHABET_BY_NUMBER[num])

    return ''.join(result)


def decryption(text, key):
    """Дешифрование текста"""
    result = []
    k = -1

    for char in text:
        if char not in ALPHABET:
            result.append(char)
            continue

        k += 1
        if k == len(key):
            k = 0

        num = ALPHABET[char] - ALPHABET[key[k]]

        if num <= 0:
            num += len(ALPHABET)

        result.append(ALPHABET_BY_NUMBER[num])

    return ''.join(result)


def main():
    try:
        with open(TEXT_ORIGINAL, 'r', encoding='utf-8') as f:
            text = f.read().strip().upper()

        with open(KEY, 'r', encoding='utf-8') as f:
            key = f.read()

        if not text:
            print("Ошибка: файл текста пуст!")
            return

        if not key:
            print("Ошибка: файл ключа пуст!")
            return

        enc_text = encryption(text, key)
        with open(TASK1_ENCRYPTION, 'w', encoding='utf-8') as f:
            f.write(enc_text)
        print("Шифрование завершено. Результат в task1_encryption.txt")

        dec_text = decryption(enc_text, key)
        with open(TASK1_DECRYPTION, 'w', encoding='utf-8') as f:
            f.write(dec_text)
        print("Расшифровка завершена. Результат в task1_decryption.txt")

        if text == dec_text:
            print("Успех: исходный и расшифрованный тексты совпадают.")
        else:
            print("Внимание: тексты не совпадают. Проверьте логику или наличие лишних символов.")

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()