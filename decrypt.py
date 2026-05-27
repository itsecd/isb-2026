import json

def decrypt(text, reverse_key):
    return "".join(reverse_key.get(ch, ch) for ch in text)

def main():
    with open("key.txt", "r", encoding="utf-8") as f:
        key = json.load(f)

    reverse_key = {value: source for source, value in key.items()}

    with open("cipher.txt", "r", encoding="utf-8") as f:
        cipher = f.read()

    plain = decrypt(cipher, reverse_key)

    with open("decrypted.txt", "w", encoding="utf-8") as f:
        f.write(plain)

    print("Готово: decrypted.txt")

if __name__ == "__main__":
    main()