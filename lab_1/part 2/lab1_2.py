import freqs

def scaning_freq(path: str) -> list:
    """Поиск частоты вхождения символов"""
    with open (path, encoding='utf-8') as f:
        text = f.read().strip().replace('\n', '')
    freq_dict = {}
    for i in text:
        freq_dict[i] = freq_dict.get(i, 0) + 1
    total = len(text)
    for i in freq_dict:
        freq_dict[i] = freq_dict[i]/total
    freq_sorted = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    with open("freq.txt", 'w', encoding='utf-8') as f:
        for i, freq in freq_sorted:
            f.write(f"{i} -> {freq}\n")
    return freq_sorted

def swap_values(cipher: list, ref: dict, output_path: str = "out_2.txt") -> dict:
    """Обмен значениями, построение ключа"""
    key_dict = {}
    length = min(len(cipher), len(ref))
    ref = sorted(ref.items(), key=lambda x: x[1], reverse=True)
    for i in range (length):
        cipher_el = cipher[i][0]
        ref_el = ref[i][0]
        key_dict[cipher_el] = ref_el
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, j in key_dict.items():
            f.write(f"{i} -> {j}\n")
    return key_dict

def decrypt_text(path: str, key: dict, output: str) -> str:
    """ Дешифровка"""
    with open (path, encoding='utf-8') as f:
        text = f.read()
    decrypted = ''
    for i in text:
        decrypted += key.get(i,i)
    with open (output, 'w', encoding='utf-8') as f:
        f.write(decrypted)
    return decrypted

def save_key(key: dict, output_path: str) -> None:
    """функция для сохранения ключа"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for k, v in key.items():
            f.write(f"{k} -> {v}\n")

def interactive_decrypt(encrypted_path: str, key: dict, output_path: str, decrypted_path: str) -> None:
    """Интерактивный режим"""
    print("\nРАСШИФРОВКА")
    print("Команды:")
    print("  swap A B  — поменять местами значения для A и B")
    print("  show      — показать текущий ключ")
    print("  text      — показать расшифрованный текст")
    print("  save      — сохранить ключ в out_2.txt")
    print("  quit      — выйти\n")
    current_key = key.copy()
    while True:
        command = input(">>> ").strip()
        if command == 'quit':
            save_key(current_key, output_path)
            decrypt_text(encrypted_path, current_key, decrypted_path)
            print("Выход из режима...")
            break
        elif command == 'show':
            print("\nТекущий ключ:")
            for k, v in sorted(current_key.items()):
                print(f"{k} -> {v}")
            print()
        elif command == 'text':
            decrypted = ''
            with open(encrypted_path, encoding='utf-8') as f:
                text = f.read()
            for c in text:
                decrypted += current_key.get(c, c)
            print("\n Расшифрованный текст:")
            print(decrypted)
        elif command == 'save':
            save_key(current_key, output_path)
            decrypt_text(encrypted_path, current_key, decrypted_path)
            print(f"Ключ сохранён в {output_path}\n")
        elif command.startswith('swap'):
            parts = command.split()
            if len(parts) != 3:
                print("Формат: swap A B\n")
                continue
            c1, c2 = parts[1], parts[2]
            if c1 not in current_key or c2 not in current_key:
                print(f"Символы не найдены в ключе\n")
                continue
            val1, val2 = current_key[c1], current_key[c2]
            current_key[c1], current_key[c2] = val2, val1
            print(f"Обмен: {c1} <-> {c2}\n")
        else:
            print(" Неизвестная команда\n")
def main() -> None:
    print("РАСШИФРОВКА\n")
    a = scaning_freq("input.txt")
    b = swap_values(a, freqs.FREQ)
    decrypt_text("input.txt", b, "decrypted.txt")
    choice = input("Запустить интерактивный режим? (y/n): ").strip()
    if choice.lower() == 'y':
        interactive_decrypt("input.txt", b, "out_2.txt", "decrypted.txt")
    print("\nГотово")


if __name__ == "__main__":
    main()




    
