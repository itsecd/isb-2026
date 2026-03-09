from collections import Counter
import json

STANDARD_FREQUENCY = {
    ' ': 0.128675, 'О': 0.096456, 'И': 0.075312, 'Е': 0.072292,
    'А': 0.064841, 'Н': 0.061820, 'Т': 0.061619, 'С': 0.051953,
    'Р': 0.040677, 'В': 0.039267, 'М': 0.029803, 'Л': 0.029400,
    'Д': 0.026983, 'Я': 0.026379, 'К': 0.025977, 'П': 0.024768,
    'З': 0.015908, 'Ы': 0.015707, 'Ь': 0.015103, 'У': 0.013290,
    'Ч': 0.011679, 'Ж': 0.010673, 'Г': 0.009867, 'Х': 0.008659,
    'Ф': 0.007249, 'Й': 0.006847, 'Ю': 0.006847, 'Б': 0.006645,
    'Ц': 0.005034, 'Ш': 0.004229, 'Щ': 0.003625, 'Э': 0.002416, 'Ъ': 0.000000
}

def analyze_frequency(text):
    """Анализирует частоту символов в тексте"""
    total = len(text)
    freq = Counter(text)
    return {char: count/total for char, count in freq.items()}

def create_decryption_key(encrypted_freq, standard_freq):
    """Создает ключ дешифровки на основе частотного анализа"""
    encrypted_sorted = sorted(encrypted_freq.keys(), 
                             key=lambda x: encrypted_freq[x], 
                             reverse=True)
    standard_sorted = sorted(standard_freq.keys(), 
                            key=lambda x: standard_freq[x], 
                            reverse=True)
    
    decrypt_key = {}
    for enc_char, std_char in zip(encrypted_sorted, standard_sorted):
        decrypt_key[enc_char] = std_char
    
    return decrypt_key

def decrypt_text(text, key):
    """Дешифрует текст используя ключ"""
    return ''.join(key.get(char, char) for char in text)

def save_frequency_table(freq, filename='frequency_table.txt'):
    """Сохраняет таблицу частот в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("ТАБЛИЦА ЧАСТОТ СИМВОЛОВ ЗАШИФРОВАННОГО ТЕКСТА\n")
        f.write(f"{'Символ':<12} {'Частота':<15} {'Процент':<12} {'Стандартная':<15}\n")
        
        for char, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
            std_freq = STANDARD_FREQUENCY.get(char, 0)
            f.write(f"'{char}'          {count:<15.6f} {count*100:<12.2f}% {std_freq:<15.6f}\n")
        f.write(f"Всего символов: {len(freq)}\n")

def main():
    with open('cod25.txt', 'r', encoding='utf-8') as f:
        encrypted_text = f.read()
    
    print(f"Зашифрованный текст: {len(encrypted_text)} символов")
    
    encrypted_freq = analyze_frequency(encrypted_text)
    decrypt_key = create_decryption_key(encrypted_freq, STANDARD_FREQUENCY)
    
    decrypted_text = decrypt_text(encrypted_text, decrypt_key)
    
    save_frequency_table(encrypted_freq)
    
    with open('decrypted_task2.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    print("Дешифрованный текст сохранен в decrypted_task2.txt")
    
    with open('found_key_task2.json', 'w', encoding='utf-8') as f:
        json.dump(decrypt_key, f, ensure_ascii=False, indent=2, sort_keys=True)
    print("Найденный ключ сохранен в found_key_task2.json")
    
    print(decrypted_text[:600])

if __name__ == "__main__":
    main()