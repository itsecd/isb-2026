from key import decrypt_key


def decrypt_text(text, decrypt_key_dict):
    """Расшифровывает текст с помощью словаря замены"""
    result = ""

    for char in text:
        if char in decrypt_key_dict:
            result += decrypt_key_dict[char]
        else:
            result += char

    return result


def main():
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    decrypted_text = decrypt_text(text, decrypt_key)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted_text)

    print(decrypted_text)


if __name__ == "__main__":
    main()
