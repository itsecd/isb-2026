from const import(
    INPUT_CIPHER_FILE, INPUT_KEY_FILE, OUTPUT_FREQUENCY_ANALYSIS, OUTPUT_DECRYPTED_TEXT, OUTPUT_DECRYPTED_ANALYSIS 
)
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

def read_key_from_file(filename):
    key_mapping = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and '->' in line:
                    parts = line.split('->')
                    if len(parts) == 2:
                        cipher_part = parts[0].strip()
                        if cipher_part == "' '" or cipher_part == '" "':
                            cipher_char = ' '
                        else:
                            cipher_char = cipher_part.strip("'\" ")
                            if not cipher_char and cipher_part:
                                cipher_char = cipher_part
                        
                        # Извлекаем символ открытого текста
                        plain_part = parts[1].strip()
                        if plain_part == "' '" or plain_part == '" "':
                            plain_char = ' '
                        else:
                            plain_char = plain_part.strip("'\" ")
                            if not plain_char and plain_part:
                                plain_char = plain_part
                        
                        if cipher_char is not None and plain_char is not None:
                            key_mapping[cipher_char] = plain_char
        return key_mapping
    except FileNotFoundError:
        print(f"Ошибка: Файл ключа '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла ключа: {e}")
        return None

def frequency_analysis(text, output_filename=None):
    chars = list(text)
    total = len(chars)
    freq = {}
    for c in chars:
        freq[c] = freq.get(c, 0) + 1
    
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    print("ЧАСТОТНЫЙ АНАЛИЗ ТЕКСТА")
    print(f"Всего символов: {total}")
    print("\nСимвол | Кол-во | Частота")
    print("-" * 30)
    for c, count in sorted_freq:
        print(f"{repr(c)[1:-1] if c.isspace() else c:6} | {count:6} | {count/total:.4f}")
    print()
    
    if output_filename:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("ЧАСТОТНЫЙ АНАЛИЗ ТЕКСТА\n")
            f.write(f"Всего символов: {total}\n")
            f.write("\nСимвол | Кол-во | Частота\n")
            f.write("-" * 30 + "\n")
            for c, count in sorted_freq:
                display_char = repr(c)[1:-1] if c.isspace() else c
                f.write(f"{display_char:6} | {count:6} | {count/total:.4f}\n")
        print(f"Частотный анализ сохранён в файл '{output_filename}'")
    
    return sorted_freq

def decrypt_text(cipher_text, key_mapping):
    decrypted = []
    for char in cipher_text:
        decrypted.append(key_mapping.get(char, char))
    return ''.join(decrypted)


def main():
    cipher_text = read_cipher_from_file(INPUT_CIPHER_FILE)
    
    if cipher_text is None:
        print("Не удалось прочитать файл. Программа завершена.")
        return
    
    print("АНАЛИЗ ИСХОДНОГО ЗАШИФРОВАННОГО ТЕКСТА")
    freq_results = frequency_analysis(cipher_text, OUTPUT_FREQUENCY_ANALYSIS)
    
    key_mapping = read_key_from_file(INPUT_KEY_FILE)
 
    decrypted_text = decrypt_text(cipher_text, key_mapping)
    
    # Сохранение дешифрованного текста
    with open(OUTPUT_DECRYPTED_TEXT, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)

    
    # Частотный анализ дешифрованного текста
    print("\n" + "="*50)
    print("АНАЛИЗ ДЕШИФРОВАННОГО ТЕКСТА")
    frequency_analysis(decrypted_text, OUTPUT_DECRYPTED_ANALYSIS)
    
    print("\nДешифровка завершена. Файлы сохранены:")
    print("- decrypted_text.txt (дешифрованный текст)")
    print("- frequency_analysis.txt (анализ исходного текста)")
    print("- decrypted_analysis.txt (анализ дешифрованного текста)")
    
    
    print(decrypted_text)

if __name__ == "__main__":
    main()
