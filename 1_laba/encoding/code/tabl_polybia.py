def encrypt(alphabet: str, text: str) -> str:

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
