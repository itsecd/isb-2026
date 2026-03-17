from consts import (
    ALPHABET
    )

def read_file(filename):
    '''Чтение файла'''
    with open(filename, 'r', encoding='cp1251') as file:
        return file.read()

def write_file(filename, data):
    '''Запись в файл'''
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def create_key(filename, encode_dict, side):
    '''Запись ключа в файл'''
    with open(filename, 'w', encoding='utf-8') as key_file:
        key_file.write(f"Алфавит: {''.join(ALPHABET)}\n")
        key_file.write(f"Размер стороны квадрата: {side}\n")
        key_file.write(f"Квадрат:\n")
        for row in encode_dict:
            key_file.write(f"{row}: {encode_dict[row]}\n")

def create_polybius_square(alphabet):
    '''Создание квадрата Полибия'''
    size = len(alphabet)
    side = int(size ** 0.5)
    if side * side < size:
        side += 1
    square = [alphabet[i * side:(i + 1) * side] for i in range(side)]
    encode_dict = {}
    decode_dict = {}
    for row_idx, row in enumerate(square, start=1):
        for col_idx, char in enumerate(row, start=1):
            code = f"{row_idx}{col_idx}"
            encode_dict[char] = code
            decode_dict[code] = char
    return encode_dict, decode_dict, side

def encrypt(text, encode_dict):
    '''Защифровка текста'''
    encrypted = ''
    for char in text:
        if char in encode_dict:
            encrypted += encode_dict[char]
        else:
            encrypted += char
    return encrypted

def decrypt(encrypted_text, decode_dict):
    '''Расшифровка текста'''
    decrypted = ''
    i = 0
    while i < len(encrypted_text):
        if i + 1 < len(encrypted_text) and encrypted_text[i].isdigit() and encrypted_text[i + 1].isdigit():
            code = encrypted_text[i:i+2]
            char = decode_dict.get(code, '')
            decrypted += char
            i += 2
        else:
            decrypted += encrypted_text[i]
            i += 1
    return decrypted

def main():
    '''Основная функция'''

    try:
        original_text = read_file('original_text_1.txt')
        #original_text = original_text.upper()
        #filtered_text = ''.join([ch for ch in original_text if ch in ALPHABET])

        encode_dict, decode_dict, side = create_polybius_square(ALPHABET)

        create_key('key_1.txt', encode_dict, side)

        encrypted_text = encrypt(original_text, encode_dict)
        write_file('encrypted_text_1.txt', encrypted_text)

        decrypted_text = decrypt(encrypted_text, decode_dict)
        write_file('decrypted_text_1.txt', decrypted_text)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    

if __name__ == '__main__':
    main()
