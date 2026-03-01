import string
from pathlib import Path

def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            print(f"Файл {file_path} загружен")
            return f.read()
    except FileNotFoundError:
        print("Файл не найден")
        return ""

def clean_text(text: str) -> str:
    text = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    text = text.replace(' ', '')
    return text

def caesar_cipher(text: str, shift: int, output_path: str = "encrypted.txt") -> str:
    result = []
    russian_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    russian_lower = russian_upper.lower()
    
    for char in text:
        if char in russian_upper:
            idx = (russian_upper.index(char) + shift) % 33
            result.append(russian_upper[idx])
        elif char in russian_lower:
            idx = (russian_lower.index(char) + shift) % 33
            result.append(russian_lower[idx])
        else:
            result.append(char)
    
    encrypted_text = ''.join(result)
    Path(output_path).write_text(encrypted_text, encoding='utf-8')
    print(f"Зашифрованный текст сохранён в {output_path}")
    return encrypted_text

def caesar_decipher(text: str, shift: int, output_path: str = "decrypted.txt") -> str:
    result = []
    russian_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    russian_lower = russian_upper.lower()
    decrypt_shift = (-shift) % 33
    
    for char in text:
        if char in russian_upper:
            idx = (russian_upper.index(char) + decrypt_shift) % 33
            result.append(russian_upper[idx])
        elif char in russian_lower:
            idx = (russian_lower.index(char) + decrypt_shift) % 33
            result.append(russian_lower[idx])
        else:
            result.append(char)
    
    decrypted_text = ''.join(result)
    Path(output_path).write_text(decrypted_text, encoding='utf-8')
    print(f"Дешифрованный текст сохранён в {output_path}")
    return decrypted_text

def main():
    input_file = "original.txt"
    
    # 1. Читаем файл
    original_text = read_file(input_file)
    print("1. Оригинальный текст:")
    print(original_text)
    print("-" * 50)
    
    # 2. Очищаем текст
    cleaned = clean_text(original_text)
    print("2. Очищенный текст:")
    print(cleaned)
    print("-" * 50)
    
    # 3. Шифруем очищенный текст
    shift = 5
    encrypted_text = caesar_cipher(cleaned, shift, "encrypted.txt")
    print("3. Зашифрованный текст:")
    print(encrypted_text)
    print("-" * 50)
    
    # 4. Дешифруем
    decrypted_text = caesar_decipher(encrypted_text, shift, "decrypted.txt")
    print("4. Дешифрованный текст:")
    print(decrypted_text)
    print("Дешифровка успешна! Текст восстановлен.")

if __name__ == "__main__":
    main()
