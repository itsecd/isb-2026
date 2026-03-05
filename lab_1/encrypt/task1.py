def encrypt_aka_decrypt(text, alphabet, cipher):
    """Шифрует текст, заменяя буквы по ключу."""
    result = ""
    for char in text.upper():
        if char in alphabet:
            result += cipher[alphabet.index(char)]
        else:
            result += char
    return result


def display_key(alphabet, cipher):
    """Показывает текущий ключ."""
    print("\n" + "="*50)
    print("ТЕКУЩИЙ КЛЮЧ ШИФРОВАНИЯ:")
    print("="*50)
    print(f"Алфавит ({len(alphabet)}): " + alphabet)
    print(f"Ключ    ({len(cipher)}): " + cipher)
    
    # Показываем соответствия
    print("\nСоответствия:")
    for i in range(0, len(alphabet), 10):
        chunk = min(10, len(alphabet) - i)
        for j in range(chunk):
            a_char = '⎵' if alphabet[i+j] == ' ' else alphabet[i+j]
            c_char = '⎵' if cipher[i+j] == ' ' else cipher[i+j]
            print(f" {a_char}->{c_char}", end="  ")
        print()


def modify_key(alphabet, cipher):
    """Позволяет пользователю изменить ключ."""
    new_cipher = list(cipher)
    
    while True:
        display_key(alphabet, "".join(new_cipher))
        
        print("\nКоманды:")
        print("  X Y  - заменить символ X на Y в ключе")
        print("  done - закончить редактирование")
        print("  exit - выйти без сохранения")
        
        cmd = input("\nВведите команду: ").strip()
        
        if cmd.lower() == 'done':
            return "".join(new_cipher)
        elif cmd.lower() == 'exit':
            return None
        elif len(cmd.split()) == 2:
            old, new = cmd.split()
            if old in new_cipher:
                idx = new_cipher.index(old)
                new_cipher[idx] = new.upper()
                print(f"Заменено: {old} -> {new.upper()}")
            else:
                print(f"Символ '{old}' не найден в ключе")
        else:
            print("Неизвестная команда")


def save_key_to_file(alphabet, cipher, filename="key.txt"):
    """Сохраняет ключ в файл."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(alphabet + "\n")
        f.write(cipher)
    print(f"Ключ сохранён в {filename}")


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        original = f.read()

    with open("key.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        alphabet = lines[0].rstrip('\n')
        cipher = lines[1].rstrip('\n')

    print(f"Длина алфавита: {len(alphabet)}")
    print(f"Длина ключа: {len(cipher)}")
    
    # Возможность изменить ключ
    while True:
        display_key(alphabet, cipher)
        
        print("\nХотите изменить ключ?")
        print("1 - да, изменить")
        print("2 - нет, использовать текущий")
        
        choice = input("Ваш выбор (1/2): ").strip()
        
        if choice == "1":
            modified = modify_key(alphabet, cipher)
            if modified:
                cipher = modified
                save_key_to_file(alphabet, cipher)
                print(" Ключ обновлён!")
            break
        elif choice == "2":
            print("Используем текущий ключ")
            break
        else:
            print("Неверный выбор. Введите 1 или 2")

    # Шифруем
    encrypted = encrypt_aka_decrypt(original, alphabet, cipher)

    with open("encrypted.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    print("Создан файл encrypted.txt")

    # Проверка
    decrypted = encrypt_aka_decrypt(encrypted, cipher, alphabet)

    print("\n" + "="*50)
    print("ПРОВЕРКА РАСШИФРОВКИ:")
    print("="*50)
    print("Исходный текст:     " + original[:100] + "..." if len(original) > 100 else original)
    print("Расшифрованный текст: " + decrypted[:100] + "..." if len(decrypted) > 100 else decrypted)
    
    if original.upper() == decrypted:
        print("\nАлгоритм работает корректно!")
    else:
        print("\nОшибка: расшифрованный текст не совпадает с исходным!")