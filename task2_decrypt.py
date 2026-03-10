# task2_decrypt.py
"""
Задание 2: Дешифровка текста из 17 варианта с помощью частотного анализа
Вариант 17: файл cod17.txt
"""

from utils import (
    RUS_ALPHABET, REFERENCE_SORTED, clean_text,
    read_file, write_file, calculate_frequencies,
    print_frequencies
)

CIPHER_TEXT_17 = """I7yO1EXXQU=E<7PUNRO9yQINOI7KEXXQUPIOI=EXQKQKEQO yT- DO=JPIiEZ=71PE0U7%7OYQOPIAX7%7OPTR<JOP7U7=KXOIHT7O9AiEZ =71JXK7OII7PITXKEQ 7IPK71KKQOU=QII71XKEOPO1EXXQU=E<XKXOA7%=EUXXOXUAP EOOIPUAEIPUE<QIPEO9AP7K7XQ=K7IPUQ3O1O1iEZ=sQX7X0P17IF KQKE0T1U81UNPIOXQOY7TYK7OTEKQ3K7IPUE0U7YQ PEX- XQU=E<XKQO1EPUQXKO1O1P17RO7<Q=QyNOyQTDUOXK0I7<XKQ OEOI7U7<XKQ O1OII7<XKIOO1EPUQXJIOO1iEZ=71XKEQO1KII7TKDUQIPDOUJAPOE1o 7yK7QOP17IFQKEQOYQTEUPIOXK0I7TPEO9JQUXOPJYYK3OE9 OKEIO- OP7yE=sQUPIOO1EPII7TN971XKEQX0I=QyQTQKX7%7OPTR<J 1OII7U7<XKIOOA7%=EUXJIOOZ7=XE=sQUPIOUJAPOXK9K1XQXD1 KIO7XKJDO%JXXXOOEO1O1I=7rQIPIOQOO%QKQ=E=71XKE7O7PsF QIPU1TDQUPIOiEZ=71XKEQOII7PITXKEJED U7OQIPUNO7XK0I7UP7XOXKAPJYK1QUPIOXK0JEO1o7yKE P 1OIO7yQO1EXXQU=E<XK7%7O1EZ=71XKEJEOUTDIOI7YIPUXK71PE0EOI Q=QIPUJXK71PE0E1o7yXKIOOYJXKXKIOO9JYQ3IPU1sRUPIOIPT7YKKQ OXK7%7s=71XQ1KQOA7%=EUXK GUEOs=71XQ3O0X7YQUOIIKUNO7<QKN0XK7%7OEOPJYYK3O1P7O P17EXOPTR<7X"""

def create_frequency_table(cipher_text):
    freq_dict, sorted_chars = calculate_frequencies(cipher_text)
    return freq_dict, sorted_chars

def initial_substitution(cipher_text, freq_sorted):
    substitution = {}
    
    for i, cipher_char in enumerate(freq_sorted):
        if i < len(REFERENCE_SORTED):
            substitution[cipher_char] = REFERENCE_SORTED[i]
        else:
            substitution[cipher_char] = '?'
    
    return substitution

def apply_substitution(text, substitution):
    result = []
    for char in text:
        if char in substitution:
            result.append(substitution[char])
        else:
            result.append(char)
    return ''.join(result)

def manual_refine_substitution(text, substitution):
    print("\n" + "="*60)
    print("ШАГ 2: УТОЧНЕНИЕ ПОДСТАНОВКИ")
    print("="*60)
    print("\nТекущий текст после частотной подстановки:")
    print("-"*60)
    print(apply_substitution(text, substitution))
    print("-"*60)
    
    substitution = substitution.copy()
    
    print("\nВводите замены в формате: символ_шифра=буква")
    print("Например: если видите, что '7' должно быть 'О', введите 7=О")
    print("Для завершения введите 'готово'")
    
    while True:
        print("\n" + apply_substitution(text, substitution))
        cmd = input("\nВведите замену: ").strip()
        
        if cmd.lower() == 'готово':
            break
        
        if '=' in cmd and len(cmd) == 3:
            cipher_char, plain_char = cmd.split('=')
            if plain_char.upper() in RUS_ALPHABET:
                substitution[cipher_char] = plain_char.upper()
                print(f"Замена {cipher_char} -> {plain_char.upper()} добавлена")
            else:
                print("Ошибка: буква должна быть из русского алфавита")
        else:
            print("Ошибка: неверный формат. Используйте формат символ=буква")
    
    return substitution

def save_key(key, filename):
    lines = ["НАЙДЕННЫЙ КЛЮЧ ШИФРОВАНИЯ:",
             "Символ шифра -> Буква русского алфавита",
             "-" * 40]
    
    for cipher_char, plain_char in sorted(key.items()):
        cipher_display = 'ПРОБЕЛ' if cipher_char == ' ' else cipher_char
        plain_display = 'ПРОБЕЛ' if plain_char == ' ' else plain_char
        lines.append(f"{cipher_display:6} -> {plain_display}")
    
    write_file(filename, '\n'.join(lines))

def main():
    print("="*60)
    print("ЗАДАНИЕ 2: ДЕШИФРОВКА ТЕКСТА (ВАРИАНТ 17)")
    print("="*60)
    
    write_file("data/task2/cod17.txt", CIPHER_TEXT_17)
    
    cipher_text = CIPHER_TEXT_17
    
    print(f"\nДлина зашифрованного текста: {len(cipher_text)} символов")
    
    freq_dict, sorted_chars = create_frequency_table(cipher_text)
    
    print_frequencies(freq_dict, "Частоты символов в зашифрованном тексте")
    
    freq_lines = ["ЧАСТОТЫ СИМВОЛОВ В ЗАШИФРОВАННОМ ТЕКСТЕ:"]
    for char, freq in sorted(freq_dict.items(), key=lambda x: x[1], reverse=True):
        char_display = 'ПРОБЕЛ' if char == ' ' else char
        freq_lines.append(f"{char_display}: {freq:.6f}")
    write_file("data/task2/frequencies.txt", '\n'.join(freq_lines))
    
    print("\n" + "="*60)
    print("ШАГ 1: ПЕРВОНАЧАЛЬНАЯ ПОДСТАНОВКА ПО ЧАСТОТАМ")
    print("="*60)
    print("Самая частая буква в шифре -> пробел")
    print("Вторая по частоте -> О")
    print("Третья -> И и т.д.")
    
    substitution = initial_substitution(cipher_text, sorted_chars)
    
    substitution = manual_refine_substitution(cipher_text, substitution)
    
    decrypted_text = apply_substitution(cipher_text, substitution)
    
    write_file("data/task2/decrypted.txt", decrypted_text)
    save_key(substitution, "data/task2/found_key.txt")
    
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТ ДЕШИФРОВКИ:")
    print("="*60)
    print(decrypted_text)
    print("="*60)
    print(f"\nРезультаты сохранены:")
    print(f"  - Зашифрованный текст: data/task2/cod17.txt")
    print(f"  - Таблица частот: data/task2/frequencies.txt")
    print(f"  - Расшифрованный текст: data/task2/decrypted.txt")
    print(f"  - Найденный ключ: data/task2/found_key.txt")

if __name__ == "__main__":
    main()