from collections import Counter
<<<<<<< HEAD
import path_file as pf
=======
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9

def load_key(filename):
    """Загружает ключ подстановки из файла"""
    key = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if '=' in line:
                idx = line.index('=')
                enc_char = line[:idx]
                dec_char = line[idx+1:]
                key[enc_char] = dec_char
    return key

def decrypt_text(encrypted_text, key):
    """Расшифровывает текст используя ключ подстановки"""
    result = []
    for char in encrypted_text:
        if char in key:
            result.append(key[char])
        else:
            result.append(char)
    return "".join(result)

def calculate_and_save_frequencies(text, filename):
    """Подсчитывает и сохраняет частоты"""
    from collections import Counter
    
    counter = Counter(text)
    total = sum(counter.values())
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Общее количество символов: {total}\n\n")
        
        for char, count in counter.most_common():
            percentage = (count / total * 100) if total > 0 else 0
            if char == ' ':
                char_display = 'пробел'
            else:
                char_display = char
            f.write(f"{char_display}: {count} ({percentage:.4f}%)\n")

def main():
    """Главная функция для задания 2"""
    print("ЗАДАНИЕ 2: РАСШИФРОВКА ТЕКСТА (ШИФР ПРОСТОЙ ПОДСТАНОВКИ)")
    
    try:
<<<<<<< HEAD
        key = load_key(pf.INPUT_KEY)
    except FileNotFoundError:
        print(f"Файл {pf.INPUT_KEY} не найден!")
        return
    
    try:
        with open(pf.INPUT_TEXT, 'r', encoding='utf-8') as f:
            encrypted_text = f.read()
    except FileNotFoundError:
        print(f"Файл {pf.INPUT_TEXT} не найден!")
=======
        key = load_key('key_task2.txt')
    except FileNotFoundError:
        print("Файл 'key_task2.txt' не найден!")
        return
    
    try:
        with open('encrypted_task2.txt', 'r', encoding='utf-8') as f:
            encrypted_text = f.read()
    except FileNotFoundError:
        print("Файл 'encrypted_task2.txt' не найден!")
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
        return
    
    calculate_and_save_frequencies(encrypted_text, "task2_frequencies.txt")
    print("Частоты сохранены в 'task2_frequencies.txt'")
    
    decrypted_text = decrypt_text(encrypted_text, key)
    
<<<<<<< HEAD
    with open(pf.OUTPUT_TEXT, "w", encoding='utf-8') as f:
=======
    with open("decrypted_task2.txt", "w", encoding='utf-8') as f:
>>>>>>> 2ab1c3a8a7fc68eb2b4b8e12e4181499f6e590f9
        f.write(decrypted_text)
    
    print("Результаты сохранены:")
    print("  - decrypted_task2.txt (расшифрованный текст)")
    print("  - task2_frequencies.txt (частоты символов)")

if __name__ == "__main__":
    main()