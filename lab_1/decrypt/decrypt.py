# Частоты букв русского языка
RUSSIAN_FREQ = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л',
               'Д', 'Я', 'К', 'П', 'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г', 'Х',  
               'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ']


def read_ciphertext(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def calculate_frequencies(text):
    freqs = {}
    total = 0
    for c in text:
        if c.isalpha() or c in '@=%<>':
            freqs[c] = freqs.get(c, 0) + 1
            total += 1
    
    sorted_freqs = sorted([(c, count/total) for c, count in freqs.items()], 
                          key=lambda x: x[1], reverse=True)
    return sorted_freqs


def create_mapping(sorted_freqs):
    mapping = {}
    for i in range(min(len(sorted_freqs), len(RUSSIAN_FREQ))):
        cipher_char = sorted_freqs[i][0]
        rus_char = RUSSIAN_FREQ[i]
        mapping[cipher_char] = rus_char
        freq_percent = sorted_freqs[i][1] * 100
        print(f"{i+1:2d} |   '{cipher_char}'   |  {freq_percent:5.2f}%  |      '{rus_char}'")
    
    print("-" * 60)
    print(f"Всего уникальных символов: {len(sorted_freqs)}")
    print(f"Использовано букв из словаря: {min(len(sorted_freqs), len(RUSSIAN_FREQ))}")
    print()
    return mapping


def decrypt_text(text, mapping):
    result = ""
    for c in text:
        result += mapping.get(c, c)
    return result


def show_frequencies(sorted_freqs, mapping):
    print("\nЧАСТОТЫ СИМВОЛОВ В ИСХОДНОМ ФАЙЛЕ:")
    print("-" * 60)
    print(" № | Символ | Частота | Текущая замена")
    print("-" * 60)
    for i, (c, f) in enumerate(sorted_freqs[:20]):
        freq_percent = f * 100
        current = mapping.get(c, "—")
        print(f"{i+1:2d} |   '{c}'   |  {freq_percent:5.2f}%  |     '{current}'")
    print("-" * 60)


def save_result(text, mapping, filename="decrypted.txt"):
    result = decrypt_text(text, mapping)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Сохранено в {filename}")


def main():
    ciphertext = read_ciphertext("cod14.txt")
    sorted_freqs = calculate_frequencies(ciphertext)
    mapping = create_mapping(sorted_freqs)
    
    print("Автоматическая замена завершена. Вводите команды:\n")
    
    while True:
        result = decrypt_text(ciphertext, mapping)
        print("\n" + "="*60)
        print(result)
        print("="*60)
        
        cmd = input("\nКоманда (X Y, del X, list, freq, save, exit): ").strip()
        
        if cmd == 'exit':
            break
            
        elif cmd == 'list':
            print("\nТекущие замены:")
            for c, r in sorted(mapping.items()):
                print(f"'{c}' -> '{r}'")
        
        elif cmd == 'freq':
            show_frequencies(sorted_freqs, mapping)
                
        elif cmd == 'save':
            save_result(ciphertext, mapping)
            
        elif cmd.startswith('del '):
            c = cmd[4:].strip()
            if c in mapping:
                del mapping[c]
                print(f"Удалена замена для '{c}'")
            else:
                print(f"Символ '{c}' не найден в заменах")
                
        elif len(cmd.split()) == 2:
            c, r = cmd.split()
            mapping[c] = r.upper()
            print(f"Добавлено: '{c}' -> '{r.upper()}'")
            
        else:
            print("Неизвестная команда. Доступные команды: X Y, del X, list, freq, save, exit")


if __name__ == "__main__":
    main()