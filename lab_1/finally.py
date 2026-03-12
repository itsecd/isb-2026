
import json

def load_decrypt_key(filename='task2_key.json'):
    """Загружает ключ дешифровки из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def decrypt_text(text, key):
    """Дешифрует текст используя ключ"""
    result = []
    missing = []
    for char in text:
        if char in key:
            result.append(key[char])
        else:
            result.append(f'[{char}]')
            if char not in missing and char not in ' \n\t':
                missing.append(char)
    return ''.join(result), missing

def main():
  
    with open('cod8.txt', 'r', encoding='utf-8') as f:
        encrypted = f.read()
    

    decrypt_key = load_decrypt_key('task2_key.json')
    
    print(f"Зашифрованный текст: {len(encrypted)} символов")
    print(f"Загружен ключ с {len(decrypt_key)} символами\n")
    
 
    decrypted, missing = decrypt_text(encrypted, decrypt_key)
    
    
    
    with open('task2_decrypted.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted)
    
    print("Дешифрованный текст сохранен в task2_decrypted.txt")
    print("ДЕШИФРОВАННЫЙ ТЕКСТ:")
    print(decrypted)

if __name__ == "__main__":
    main()