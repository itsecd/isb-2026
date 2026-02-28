import os

def load_text(filename):
    """Загружает текст из файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def load_key(filename):
    """Загружает ключ из файла в формате 'символ -> буква'"""
    key = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '->' in line:
                parts = line.split('->')
                cipher_char = parts[0].strip()
                text_char = parts[1].strip()
                key[cipher_char] = text_char
    return key

def analyze_frequency(text):
    """Анализирует частоту символов в тексте и сохраняет в файл"""
    text_plain = text.replace('\n', '')
    total_chars = len(text_plain)
 
    freq = {}
    for char in text_plain:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    sorted_chars = []
    for char in freq:
        sorted_chars.append((freq[char], char))
    sorted_chars.sort(reverse=True)

    with open('frequency_analysis.txt', 'w', encoding='utf-8') as f:
        for count, char in sorted_chars:
            percent = (count / total_chars) * 100
            f.write(f"{char} {percent:.2f}\n")

def decrypt_text(encrypted_text, key):
    """Дешифрует текст по заданному ключу"""
    decrypted = []
    for char in encrypted_text:
        if char in key:
            decrypted.append(key[char])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def save_text(filename, text):
    """Сохраняет текст в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    ciphertext = load_text('cod1.txt')
    
    key = load_key('key.txt')
    
    analyze_frequency(ciphertext)
    
    decrypted = decrypt_text(ciphertext, key)
    
    save_text('decoded_text.txt', decrypted)

if __name__ == "__main__":
    main()