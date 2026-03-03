def read_cipher_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

input_filename = "cipher_text.txt"  

cipher_text = read_cipher_from_file(input_filename)

if cipher_text is None:
    print("Не удалось прочитать файл. Программа завершена.")
    exit()

chars = list(cipher_text)
total = len(chars)

freq = {}
for c in chars:
    freq[c] = freq.get(c, 0) + 1

sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

print("ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА")
print(f"Всего символов: {total}")
print("\nСимвол | Кол-во | Частота")
print("-" * 30)
for c, count in sorted_freq:
    print(f"{c:6} | {count:6} | {count/total:.4f}")
print()

with open('frequency_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("ЧАСТОТНЫЙ АНАЛИЗ ЗАШИФРОВАННОГО ТЕКСТА\n")
    f.write(f"Всего символов: {total}\n")
    f.write("\nСимвол | Кол-во | Частота\n")
    f.write("-" * 30 + "\n")
    for c, count in sorted_freq:
        f.write(f"{c:6} | {count:6} | {count/total:.4f}\n")

print("Частотный анализ сохранён в файл 'frequency_analysis.txt'")

cipher = cipher_text

text = cipher.replace('A', ' ')          # Пробел
text = text.replace('Y', 'О')
text = text.replace('t', 'М')
text = text.replace('-', 'И')
text = text.replace('S', 'Н')
text = text.replace('J', 'Т')
text = text.replace('E', 'Ш')
text = text.replace('$', 'Е')           
text = text.replace('F', 'Ь')
text = text.replace('U', 'Ф')
text = text.replace('I', 'Р')
text = text.replace('L', 'А')
text = text.replace('C', 'Э')
text = text.replace('Q', 'С')
text = text.replace('O', 'Л')
text = text.replace('x', 'В')
text = text.replace('M', 'Ж')
text = text.replace('n', 'Ч')
text = text.replace('8', 'Д')
text = text.replace('!', 'З')
text = text.replace('G', 'П')
text = text.replace('W', 'У')
text = text.replace('d', 'Х')
text = text.replace('Z', 'Г')
text = text.replace('=', 'Й')
text = text.replace('3', 'Ы')
text = text.replace('h', 'Б')
text = text.replace('R', 'Я')
text = text.replace('>', 'Ц')
text = text.replace('B', 'Ю')
text = text.replace('9', 'Щ')


with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)


key_mapping = {
    'A': ' ', 'Y': 'О', 't': 'М', '-': 'И', 'S': 'Н', 'J': 'Т', 'E': 'Ш',
    '$': 'Е', 'F': 'Ь', 'U': 'Ф', 'I': 'Р', 'L': 'А', 'C': 'Э', 'Q': 'С',
    'O': 'Л', 'x': 'В', 'M': 'Ж', 'n': 'Ч', '8': 'Д', '!': 'З', 'G': 'П',
    'W': 'У', 'd': 'Х', 'Z': 'Г', '=': 'Й', '3': 'Ы', 'h': 'Б', 'R': 'Я',
    '>': 'Ц', 'B': 'Ю', '9': 'Щ'
}

# Сохранение ключа шифрования
with open('cipher_key.txt', 'w', encoding='utf-8') as f:
    f.write("КЛЮЧ ШИФРОВАНИЯ\n")
    f.write("Символ шифротекста -> Буква открытого текста\n")
    f.write("-" * 50 + "\n")
    for cipher_char in sorted(key_mapping.keys()):
        plain_char = key_mapping[cipher_char]
        f.write(f"'{cipher_char}' -> '{plain_char}'\n")

print("Дешифровка завершена. Файлы сохранены:")
print(text)