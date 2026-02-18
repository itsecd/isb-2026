def encrypt(text, alphabet, cipher):
    """Шифрует текст, заменяя буквы по ключу."""
    result = ""
    for char in text.upper():
        if char in alphabet:
            result += cipher[alphabet.index(char)]
        else:
            result += char
    return result


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        original = f.read()

    with open("key.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        alphabet = lines[0].strip() 
        cipher = lines[1].strip()    

    encrypted = encrypt(original, alphabet, cipher)

    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    print("Создан файл encrypted.txt")