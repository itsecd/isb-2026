"""
Задание 1: Шифрование текста шифром простой подстановки

Изменения:
- Добавлены докстринги
- Текст вынесен в отдельный файл
- Добавлена загрузка ключа из файла
- Убраны эмодзи
"""

import random
from utils import RUS_ALPHABET, clean_text, write_file, read_file

def generate_random_key() -> dict:
    """
    Генерирует случайный ключ шифрования.
    
    Returns:
        Словарь {исходная_буква: зашифрованная_буква}
    """
    shuffled = list(RUS_ALPHABET)
    random.shuffle(shuffled)
    
    key = {}
    for i, char in enumerate(RUS_ALPHABET):
        key[char] = shuffled[i]
    
    return key

def load_key_from_file(filename: str) -> dict | None:
    """
    Загружает ключ из файла.
    
    Args:
        filename: Путь к файлу с ключом
        
    Returns:
        Ключ или None если файл не найден
    """
    content = read_file(filename)
    if not content:
        return None
    
    key = {}
    for line in content.split('\n'):
        if '->' in line and 'КЛЮЧ' not in line and 'Исходная' not in line:
            parts = line.split('->')
            if len(parts) == 2:
                orig = parts[0].strip()
                enc = parts[1].strip()
                
                if orig == 'ПРОБЕЛ':
                    orig = ' '
                if enc == 'ПРОБЕЛ':
                    enc = ' '
                
                key[orig] = enc
    
    return key if key else None

def save_key(key: dict, filename: str) -> None:
    """
    Сохраняет ключ в файл в читаемом формате.
    
    Args:
        key: Ключ шифрования
        filename: Путь для сохранения
    """
    lines = ["КЛЮЧ ШИФРОВАНИЯ (моноалфавитная замена):",
             "Исходная буква -> Зашифрованная буква",
             "-" * 40]
    
    for original, encrypted in sorted(key.items()):
        orig_display = 'ПРОБЕЛ' if original == ' ' else original
        enc_display = 'ПРОБЕЛ' if encrypted == ' ' else encrypted
        lines.append(f"{orig_display:6} -> {enc_display}")
    
    write_file(filename, '\n'.join(lines))

def encrypt(text: str, key: dict) -> str:
    """
    Шифрует текст согласно ключу.
    
    Args:
        text: Исходный текст
        key: Ключ шифрования
        
    Returns:
        Зашифрованный текст
    """
    encrypted = []
    for char in text:
        if char in key:
            encrypted.append(key[char])
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def main():
    """Основная функция программы."""
    print("=" * 60)
    print("ЗАДАНИЕ 1: ШИФРОВАНИЕ ТЕКСТА")
    print("=" * 60)
    
    # Читаем исходный текст из файла
    original_text = read_file("data/task1/original.txt")
    if original_text is None:
        print("\nОшибка: файл data/task1/original.txt не найден!")
        return
    
    # Очищаем текст
    cleaned_text = clean_text(original_text)
    print(f"\nДлина текста: {len(cleaned_text)} символов")
    
    # Проверяем наличие ключа для загрузки
    key = None
    input_key = read_file("data/task1/input_key.txt")
    if input_key:
        key = load_key_from_file("data/task1/input_key.txt")
        if key:
            print("Ключ загружен из файла input_key.txt")
    
    # Если ключ не загружен, генерируем новый
    if not key:
        key = generate_random_key()
        print("Сгенерирован новый случайный ключ")
    
    # Шифруем текст
    encrypted_text = encrypt(cleaned_text, key)
    
    # Сохраняем результаты
    write_file("data/task1/encrypted.txt", encrypted_text)
    save_key(key, "data/task1/key.txt")
    
    print(f"\nРезультаты сохранены:")
    print(f"  - Зашифрованный текст: data/task1/encrypted.txt")
    print(f"  - Ключ шифрования: data/task1/key.txt")
    
    # Проверка обратимости
    reverse_key = {v: k for k, v in key.items()}
    decrypted_check = encrypt(encrypted_text, reverse_key)
    if decrypted_check == cleaned_text:
        print(f"\nПроверка пройдена: текст успешно расшифровывается обратно")
    else:
        print(f"\nОшибка: текст не совпадает при расшифровке")

if __name__ == "__main__":
    main()