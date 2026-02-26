import constants

def load_text_from_file(filename):
    """Читает исходный текст из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()
        
def load_key_from_file(filename):
    """Загружает ключевое слово из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    words = content.split()
    return words[-1].strip() if words else ''

def char_to_index(char):
     """Преобразует символ в индекс в алфавите"""
    return alphabet.index(char)

def index_to_char(index):
    """Преобразует индекс обратно в символ"""
    return alphabet[index % len(alphabet)]

def encryption(text, keyword):
    """Шифрует текст методом Виженера"""
    text = text.upper()
    keyword = keyword.upper()
    key_indices = [char_to_index(k) for k in keyword if k in alphabet]

    result = []
    key_pos = 0

    for char in text:
        if char in alphabet:
            shift = key_indices[key_pos % len(key_indices)]
            enc_idx = (char_to_index(char) + shift) % len(alphabet)
            result.append(index_to_char(enc_idx))
            key_pos += 1
        else:
            result.append(char)

    return ''.join(result)

def main():
    try:
        keyword = load_key_from_file('task1_key.txt')
        original_text = load_text_from_file('task1_original.txt')

        if not keyword:
            print("Ошибка: ключ не найден в файле task1_key.txt")
            return

        encrypted_text = encryption(original_text, keyword)

        with open('task1_encryption.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted_text)

        print("Шифрование успешно завершено")

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден — {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
