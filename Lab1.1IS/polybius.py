import config

def load_polybius_square(filename):
    """Загружаем квадрат Полибия из файла 5x5 (пробел оставил перенес на несуществующую 6 строку)"""
    square = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    row = line.strip().split()
                    square.append(row)
        return square
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")

def load_plaintext(filename):
    """Загружаем исходный текст из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def process_text(text):
    """Подготавливаем текст для шифровки"""
    text = text.upper()
    text = text.replace('J', 'I')
    return text

def encrypt_polybius(text, square):
    """Шифрует текст с использованием квадрата Полибия"""
    char_to_pos = {}
    for r in range(5):
        for c in range(5):
            char_to_pos[square[r][c]] = f"{r+1}{c+1}"
    
    encrypted = []
    for ch in text:
        if ch == ' ':
            encrypted.append('61')
        elif ch in char_to_pos:
            encrypted.append(char_to_pos[ch])
        else:
            encrypted.append(ch)
    
    return ' '.join(encrypted)

def decrypt_polybius(encrypted_text, square):
    """Дешифруем текст из числового представления"""
    pos_to_char = {}
    for r in range(5):
        for c in range(5):
            pos_to_char[f"{r+1}{c+1}"] = square[r][c]
    
    parts = encrypted_text.split()
    decrypted = []
    
    for part in parts:
        if part == '61':
            decrypted.append(' ')
        elif len(part) == 2 and part.isdigit():
            decrypted.append(pos_to_char[part])
        else:
            decrypted.append(part) 
    
    return ''.join(decrypted)

def save_text(filename, text):
    """Сохраняем текст в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    try:
        square = load_polybius_square(config.KEY_FILE_TASK1)
        plaintext = load_plaintext(config.INPUT_FILE_TASK1)
        
        processed_text = process_text(plaintext)
        encrypted = encrypt_polybius(processed_text, square)
        decrypted = decrypt_polybius(encrypted, square)
        
        save_text(config.ENCRYPTED_OUTPUT_TASK1, encrypted)
        save_text(config.PROCESSED_OUTPUT_TASK1, processed_text)
        save_text(config.DECRYPTED_OUTPUT_TASK1, decrypted)
    
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()
