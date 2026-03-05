def equal(path_original: str, path_deciphered: str) -> bool:
    """
    :param path_original: путь до изначального текста
    :param path_deciphered: путь до расшифрованного текста
    :return: проверяет два текста на сходимость
    """
    original = ""
    deciphered = ""

    with open(path_original, 'r', encoding='utf-8') as file:
        original = file.read()
    with open(path_deciphered, 'r', encoding='utf-8') as file:
        deciphered = file.read()

    return original == deciphered

#подстановка(цезарь)
def cipher_caesar(path_txt: str, key: str) -> None:
    """
    :param path_txt: путь до текста для кодирования
    :param key: ключ для кодирования
    :return: кодировует по цезарю и сохраняет ключ и текст
    """
    text = ""
    cipher_text = ""

    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    with open(path_txt, 'r', encoding='utf-8') as file:
        text = file.read()

    j = 0
    for i in text:
        if i.isalpha():
            n = (alph.find(i.lower()) + int(key[j]))%33

            if i.lower() == i:
                cipher_text += alph[n]
            else:
                cipher_text += alph[n].upper()

            j = (j + 1) % len(key)

        else:
            cipher_text += i

    with open("ciphered_" + key + ".txt", 'w', encoding='utf-8') as file:
        file.write(cipher_text)
    with open("key_" + key + ".txt", 'w', encoding='utf-8') as file:
        file.write(key)

def decipher_caesar(path_txt: str, path_key: str) -> None:
    """
    :param path_txt: путь до текста для расшифровки
    :param path_key: пудь до ключа
    :return: сохраняет расшифрованный текст
    """
    cipher_text = ""
    key = ""
    deciphered_text = ""

    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    with open(path_txt, 'r', encoding='utf-8') as file:
        cipher_text = file.read()
    with open(path_key, 'r', encoding='utf-8') as file:
        key = file.read()

    j = 0
    for i in cipher_text:
        if i.isalpha():
            n = (alph.find(i.lower()) - int(key[j]))%33

            if i.lower() == i:
                deciphered_text += alph[n]
            else:
                deciphered_text += alph[n].upper()

            j = (j + 1) % len(key)

        else:
            deciphered_text += i

    with open("deciphered_text_" + key + ".txt", 'w', encoding='utf-8') as file:
        file.write(deciphered_text)

#cipher_caesar("orig.txt", "1221")
#decipher_caesar("ciphered_1221.txt", 'key_1221.txt')

#print(equal("orig.txt", "deciphered_text_1221.txt"))