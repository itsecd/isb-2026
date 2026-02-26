import ast
def decrypt_text(key : str, text : str) -> str:
    crypto_key = ast.literal_eval(key)

    plaintext = "".join(crypto_key.get(char,char) for char in text)

    return plaintext

def get_freq(text:str) -> str:
    len_t = len(text)
    char_freq = {i: text.count(i)/len_t for i in text}
    freq_char = {key: value for key, value in sorted(char_freq.items(), key= lambda item: item[1], reverse=True)}
    return str(freq_char)

def write_file(path : str,text : str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def open_file(path : str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    encrypted_text = open_file("cod18.txt")
    key = open_file("key_2.txt")
    print(f"Зашифрованный текст:\n{encrypted_text}\n")
    print(f"Расшифрованный текст:\n{decrypt_text(key,encrypted_text)}")
    write_file("frequency.txt", get_freq(encrypted_text))
    write_file("decrypted_2.txt", decrypt_text(key,encrypted_text))


if __name__ == "__main__":
    main()
