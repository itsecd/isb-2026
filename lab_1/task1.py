
import json
import random
import os


ALPHABET = "АБВГДЕЖЗИЙКЛМОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

def create_substitution_key():
    """
    Создаёт случайный ключ для шифра простой подстановки.
    
    """
    alphabet_list = list(ALPHABET)
    shuffled = alphabet_list.copy()
    random.shuffle(shuffled)
    return dict(zip(alphabet_list, shuffled))

def save_key(key, filename='key_task1.json'):
    """Сохраняет ключ шифрования в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(key, f, ensure_ascii=False, indent=2, sort_keys=True)

def load_key(filename='key_task1.json'):
    """Загружает ключ шифрования из JSON файла"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            key = json.load(f)
        print(f" Ключ загружен из {filename}")
        return key
    else:
        print(f" Файл {filename} не найден")
        return None

def encrypt_text(text, key):
    """
    Шифрует текст используя ключ подстановки.
    """
    encrypted = []
    for char in text.upper():
        if char in key:
            encrypted.append(key[char])
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def decrypt_text(text, key):
    """
    Дешифрует текст используя обратный ключ.
    """
    reverse_key = {v: k for k, v in key.items()}
    decrypted = []
    for char in text:
        if char in reverse_key:
            decrypted.append(reverse_key[char])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def main():
    """
    Главная функция — запускает весь процесс шифрования.
    """
    with open('task1_text.txt', 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    print(f"Исходный текст: {len(original_text)} символов")
    
    key = load_key('key_task1.json')
    
    if key is None:
        print("Создаем новый ключ шифрования")
        random.seed(42)
        key = create_substitution_key()
        save_key(key, 'key_task1.json')
    else:
        print("Используем существующий ключ")
    
    encrypted_text = encrypt_text(original_text, key)
    
    with open('task1_orig.txt', 'w', encoding='utf-8') as f:
        f.write(original_text)
    
    with open('task1_encryp.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
    
    decrypted = decrypt_text(encrypted_text, key)
    assert decrypted == original_text.upper(), "Ошибка при проверке!"
    print("Проверка дешифровки успешна")
    

if __name__ == "__main__":
    main()