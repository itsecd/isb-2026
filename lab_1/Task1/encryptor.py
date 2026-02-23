from key import decrypt_key


def create_encrypt_key(decrypt_key_dict):
    """Создаёт обратный словарь для шифрования"""
    encrypt_key = {}
    for key, value in decrypt_key_dict.items():
        encrypt_key[value] = key
    return encrypt_key


def encrypt_text(text, encrypt_key_dict):
    """Шифрует текст с помощью словаря замены"""
    result = ''
    for char in text:
        if char in encrypt_key_dict:
            result += encrypt_key_dict[char]
        else:
            result += char
    return result


def main():
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.upper()
    encrypt_key = create_encrypt_key(decrypt_key)
    encrypted_text = encrypt_text(text, encrypt_key)
    
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)


if __name__ == "__main__":
    main()