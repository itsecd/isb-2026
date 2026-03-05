ALPH = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
DEFAULT_KEY = 'ЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЕДГВБА '
def load_original_text(filename):
    """
    Загружает исходный текст из файла.
    
    Args:
        filename (str): Имя файла с исходным текстом
        
    Returns:
        str: Содержимое файла в верхнем регистре
        
    Raises:
        FileNotFoundError: Если файл не найден
        UnicodeDecodeError: Если возникла ошибка кодировки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().upper()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        raise
    except UnicodeDecodeError:
        print(f"Ошибка: Не удалось прочитать файл '{filename}' - проблема с кодировкой")
        raise

def get_key_from_user(alph_length):
    """
    Получает ключ от пользователя или использует ключ по умолчанию.
    
    Args:
        alph_length (int): Длина алфавита
        
    Returns:
        str: Ключ для шифрования
    """
    print('Алфавит:', ALPH)
    print('\nКлюч по умолчанию:', DEFAULT_KEY)
    print('(Нажмите Enter, чтобы использовать его, или введите свой ключ)')
    
    try:
        user_key = input('Ваш ключ: ').upper()
    except EOFError:
        print("\nОшибка ввода, используется ключ по умолчанию")
        return DEFAULT_KEY
    
    if user_key == '':
        return DEFAULT_KEY
    
    if len(user_key) != alph_length:
        print(f'Ошибка! Длина ключа должна быть {alph_length} символов')
        print('Будет использоваться ключ по умолчанию')
        return DEFAULT_KEY
    
    return user_key

def create_cipher_dict(alph, key):
    """
    Создает словарь для шифрования.
    
    Args:
        alph (str): Алфавит
        key (str): Ключ
        
    Returns:
        dict: Словарь для шифрования {символ_алфавита: символ_ключа}
    """
    cipher_dict = {}
    for i in range(len(alph)):
        cipher_dict[alph[i]] = key[i]
    return cipher_dict

def create_decipher_dict(alph, key):
    """
    Создает словарь для дешифровки.
    
    Args:
        alph (str): Алфавит
        key (str): Ключ
        
    Returns:
        dict: Словарь для дешифровки {символ_ключа: символ_алфавита}
    """
    decipher_dict = {}
    for i in range(len(alph)):
        decipher_dict[key[i]] = alph[i]
    return decipher_dict

def encrypt_text(text, cipher_dict):
    """
    Шифрует текст с использованием словаря замен.
    
    Args:
        text (str): Исходный текст
        cipher_dict (dict): Словарь для шифрования
        
    Returns:
        str: Зашифрованный текст
    """
    encrypted = ''
    for char in text:
        if char in cipher_dict:
            encrypted += cipher_dict[char]
        else:
            encrypted += char
    return encrypted

def decrypt_text(text, decipher_dict):
    """
    Дешифрует текст с использованием словаря замен.
    
    Args:
        text (str): Зашифрованный текст
        decipher_dict (dict): Словарь для дешифровки
        
    Returns:
        str: Расшифрованный текст
    """
    decrypted = ''
    for char in text:
        if char in decipher_dict:
            decrypted += decipher_dict[char]
        else:
            decrypted += char
    return decrypted

def save_results(encrypted_text, key, alph, decrypted_text, original_text):
    """
    Сохраняет результаты шифрования в файлы.
    
    Args:
        encrypted_text (str): Зашифрованный текст
        key (str): Использованный ключ
        alph (str): Алфавит
        decrypted_text (str): Расшифрованный текст для проверки
        original_text (str): Исходный текст
    """
    try:
        with open('encrypted.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
        
        with open('key.txt', 'w', encoding='utf-8') as f:
            f.write(f'Алфавит: {alph}\n')
            f.write(f'Ключ:    {key}\n')
            f.write(f'\nПроверка: расшифрованный текст совпадает с исходным? {decrypted_text == original_text}')
    except IOError as e:
        print(f"Ошибка при сохранении файлов: {e}")

def main():
    """
    Основная функция программы.
    """
    try:
        text = load_original_text('original.txt')
    except (FileNotFoundError, UnicodeDecodeError):
        return
    
    key = get_key_from_user(len(ALPH))
    
    print('\nИспользуемый ключ:', key)
    
    cipher_dict = create_cipher_dict(ALPH, key)
    encrypted = encrypt_text(text, cipher_dict)
    
    decipher_dict = create_decipher_dict(ALPH, key)
    decrypted = decrypt_text(encrypted, decipher_dict)
    
    save_results(encrypted, key, ALPH, decrypted, text)
    
    print('\n')
    print('Проверка:')
    print('Первые 100 символов исходного текста:')
    print(text[:100])
    print('\nПервые 100 символов после расшифровки:')
    print(decrypted[:100])
    
    if decrypted == text:
        print('\nРасшифрованный текст полностью совпадает с исходным')
    else:
        print('\nРасшифрованный текст не совпадает с исходным')
    
    print('Зашифрованный текст: encrypted.txt')
    print('Ключ шифрования: key.txt')

if __name__ == "__main__":
    main()