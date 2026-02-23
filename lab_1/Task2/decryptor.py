from collections import Counter

RU = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л', 'Д', 'Я', 'К', 'П', 'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г', 'Х', 'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ']

def count_char_frequency(text):
    total = len(text)
    frequency = Counter(text)
    with open('frequency.txt', 'w', encoding='utf-8') as f:
        for char, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True):
            percent = count / total if total > 0 else 0
            f.write(f"{char} = {percent:.4f}\n")
    return frequency

def create_decrypt_key(frequency):
    sorted_chars = [char for char, count in frequency.most_common()]
    decrypt_key = {}
    for i, char in enumerate(sorted_chars):
        if i < len(RU):
            decrypt_key[char] = RU[i]
    return decrypt_key

def save_key(decrypt_key):
    with open('first_key.txt', 'w', encoding='utf-8') as f:
        for k, v in decrypt_key.items():
            f.write(f"{k} : {v}\n")

def decrypt_text(text, decrypt_key):
    return ''.join(decrypt_key.get(char, char) for char in text) #для каждого символа сверяет его наличие в словаре

def load_right_key():
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