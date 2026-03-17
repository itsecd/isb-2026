import const

def frequency_analysis(text: str, output_filename: str = None) -> list:
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


def decrypt_file() -> str:
    key_mapping = {}
    with open(const.KEY_FILE, 'r', encoding=const.ENCODING) as key_file:
        for line in key_file:
            line = line.strip()
            if line and '->' in line:
                parts = line.split('->')
                cipher_char = parts[0].strip().strip("'\"")
                plain_char = parts[1].strip().strip("'\"")
                key_mapping[cipher_char] = plain_char

    # Чтение зашифрованного текста
    with open(const.INPUT_ENCRYPTED_FILE, 'r', encoding=const.ENCODING) as encrypted_file:
        encrypted_text = encrypted_file.read()

    # Расшифровка текста
    decrypted_text = ''
    for char in encrypted_text:
        if char in key_mapping:
            decrypted_text += key_mapping[char]
        else:
            decrypted_text += char

    # Запись расшифрованного текста в файл
    with open(const.OUTPUT_DECRYPTED_FILE_2, 'w', encoding=const.ENCODING) as decrypted_file:
        decrypted_file.write(decrypted_text)

    print(f"Расшифровка завершена. Результат сохранен в {const.OUTPUT_DECRYPTED_FILE_2}")
    
    return decrypted_text


def main() -> None:
    decrypted_text = decrypt_file()
    
    print("АНАЛИЗ ДЕШИФРОВАННОГО ТЕКСТА")
    frequency_analysis(decrypted_text, const.OUTPUT_DECRYPTED_ANALYSIS)


if __name__ == "__main__":
    main()