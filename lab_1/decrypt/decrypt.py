# Частоты букв русского языка
RUSSIAN_FREQ = [' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л',
               'Д', 'Я', 'К', 'П', 'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г', 'Х',  
               'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ']


with open("cod14.txt", "r", encoding="utf-8") as f:
    ciphertext = f.read()


freqs = {}
total = 0
for c in ciphertext:
    if c.isalpha() or c in '@=%<>':
        freqs[c] = freqs.get(c, 0) + 1
        total += 1


sorted_freqs = sorted([(c, count/total) for c, count in freqs.items()], 
                      key=lambda x: x[1], reverse=True)


# Создаём сопоставление
mapping = {}
for i in range(min(len(sorted_freqs), len(RUSSIAN_FREQ))):
    cipher_char = sorted_freqs[i][0]
    rus_char = RUSSIAN_FREQ[i]
    mapping[cipher_char] = rus_char
    # Выводим строку таблицы
    freq_percent = sorted_freqs[i][1] * 100
    print(f"{i+1:2d} |   '{cipher_char}'   |  {freq_percent:5.2f}%  |      '{rus_char}'")

print("-" * 60)
print(f"Всего уникальных символов: {len(sorted_freqs)}")
print(f"Использовано букв из словаря: {min(len(sorted_freqs), len(RUSSIAN_FREQ))}")
print()

print("Автоматическая замена завершена. Вводите команды:\n")

while True:
    # Показываем текущий текст
    result = ""
    for c in ciphertext:
        result += mapping.get(c, c)
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
        print("\nЧАСТОТЫ СИМВОЛОВ В ИСХОДНОМ ФАЙЛЕ:")
        print("-" * 60)
        print(" № | Символ | Частота | Текущая замена")
        print("-" * 60)
        for i, (c, f) in enumerate(sorted_freqs[:20]):
            freq_percent = f * 100
            current = mapping.get(c, "—")
            print(f"{i+1:2d} |   '{c}'   |  {freq_percent:5.2f}%  |     '{current}'")
        print("-" * 60)
            
    elif cmd == 'save':
        with open("decrypted.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Сохранено в decrypted.txt")
        
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