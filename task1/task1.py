alphabet = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5,
    'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9, 'И': 10,
    'Й': 11, 'К': 12, 'Л': 13, 'М': 14, 'Н': 15,
    'О': 16, 'П': 17, 'Р': 18, 'С': 19, 'Т': 20,
    'У': 21, 'Ф': 22, 'Х': 23, 'Ц': 24, 'Ч': 25,
    'Ш': 26, 'Щ': 27, 'Ъ': 28, 'Ы': 29, 'Ь': 30,
    'Э': 31, 'Ю': 32, 'Я': 33, '.': 34, ',': 35, '-': 36, ' ': 37
}

alphabet_by_number = {i: k for k, i in alphabet.items()}


def encryption(text, key):
    result = []
    k = -1
    key_len = len(key)

    for char in text:
        if char not in alphabet:
            result.append(char)
            continue

        k += 1
        if k == key_len:
            k = 0

        num = alphabet[char] + alphabet[key[k]]

        if num > len(alphabet):
            num -= len(alphabet)

        result.append(alphabet_by_number[num])

    return ''.join(result)


def decryption(text, key):
    result = []
    k = -1

    for char in text:
        if char not in alphabet:
            result.append(char)
            continue

        k += 1
        if k == len(key):
            k = 0

        num = alphabet[char] - alphabet[key[k]]

        if num <= 0:
            num += len(alphabet)

        result.append(alphabet_by_number[num])

    return ''.join(result)


def main():
    try:
        with open('text1_original.txt', 'r', encoding='utf-8') as f:
            text = f.read().strip().upper()

        with open('key.txt', 'r', encoding='utf-8') as f:
            key = f.read()

        if not text:
            print("Ошибка: файл текста пуст!")
            return

        if not key:
            print("Ошибка: файл ключа пуст!")
            return

        enc_text = encryption(text, key)
        with open('task1_encryption.txt', 'w', encoding='utf-8') as f:
            f.write(enc_text)
        print("Шифрование завершено. Результат в task1_encryption.txt")

        dec_text = decryption(enc_text, key)
        with open('task1_decryption.txt', 'w', encoding='utf-8') as f:
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