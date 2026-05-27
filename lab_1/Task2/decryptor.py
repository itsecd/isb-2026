from collections import Counter

from rus import RU


def count_char_frequency(text):
    """Подсчитывает частоту появления каждого символа в тексте"""
    total = len(text)
    frequency = Counter(text)
    with open('frequency.txt', 'w', encoding='utf-8') as f:
        for char, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True):
            percent = count / total if total > 0 else 0
            f.write(f"{char} = {percent:.4f}\n")
    return frequency

def create_decrypt_key(frequency):
    """Создает ключ дешифрования на основе частотного анализа"""
    sorted_chars = [char for char, count in frequency.most_common()]
    decrypt_key = {}
    for i, char in enumerate(sorted_chars):
        if i < len(RU):
            decrypt_key[char] = RU[i]
    return decrypt_key

def save_key(decrypt_key):
    """Сохраняет ключ дешифрования в файл"""
    with open('first_key.txt', 'w', encoding='utf-8') as f:
        for k, v in decrypt_key.items():
            f.write(f"{k} : {v}\n")

def decrypt_text(text, decrypt_key):
    """Дешифрует текст, используя ключ дешифрования"""
    return ''.join(decrypt_key.get(char, char) for char in text)

def load_right_key():
    """агружает правильный ключ"""
    right_key = {}
    with open('right_key.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key_char, value_char = line.split(':', 1)
                key_char = key_char.strip()
                value_char = value_char.strip()
                if key_char:
                    right_key[key_char] = value_char if value_char else ' '
    return right_key

def save_right_result(decrypted_text):
    """Сохраняет правильно расшифрованный текст"""
    with open('right_result.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)

def main():
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    frequency = count_char_frequency(text)
    decrypt_key = create_decrypt_key(frequency)
    save_key(decrypt_key)

    decrypted_text = decrypt_text(text, decrypt_key)
    with open('first_result.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)

    right_key = load_right_key()
    right_decrypted_text = decrypt_text(text, right_key)
    save_right_result(right_decrypted_text)

if __name__ == "__main__":
    main() 
