def encrypt(alphabet: str, text: str) -> str:
    """Шифрование текста квадратом Птолемея"""

    encrypt_dic = {}

    text_another = ""

    for index, char in enumerate(alphabet):
        row = (index // 6) + 1
        col = (index % 6) + 1
        encrypt_dic[char] = str(row) + str(col)

    for char in text.upper():
        code = encrypt_dic.get(char, char)

        text_another += code

    return text_another

def decrypt(alphabet: str, text: str) -> str:
    """Дешифрование текста, зашифрованного квадратом Птолемея"""
    decrypt_dic = {}

    for index, char in enumerate(alphabet):
        row = (index // 6) + 1
        col = (index % 6) + 1
        decrypt_dic[str(row) + str(col)] = char

    text_another = ""

    i = 0
    while i < len(text):
        pair = text[i : i + 2]
        if pair in decrypt_dic:
            text_another += decrypt_dic[pair]
            i += 2
        else:
            text_another += text[i]
            i += 1

    return text_another
