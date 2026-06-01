import os
import sys
import utilities
import RSA
import SM4


def ensure_directory_exists(file_path: str) -> None:
    """Создаёт директорию для файла, если её нет."""
    d = os.path.dirname(file_path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def show_hex_dump(data: bytes) -> str:
    """Возвращает полный hex-дамп всех байтов."""
    if not data:
        return "<пусто>"
    return ' '.join(f"{b:02x}" for b in data)


def show_text(data: bytes) -> str:
    """Возвращает полный декодированный текст."""
    if not data:
        return "<пусто>"
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return "<не удалось декодировать как UTF-8>"


def load_config(settings_path: str) -> dict:
    """Загружает конфигурацию из JSON и проверяет наличие исходного файла."""
    config = utilities.read_json(settings_path)
    if not config:
        print("[!] Не удалось загрузить конфигурацию. Завершение.")
        sys.exit(1)

    print(f"\n=== Конфигурация загружена из {settings_path} ===")
    for k, v in config.items():
        print(f"  {k}: {v}")

    if not os.path.exists(config.get("initial_file", "")):
        print(f"[!] Предупреждение: исходный файл '{config.get('initial_file')}' не найден.")
    return config


def choose_initial_file(config: dict) -> str:
    """Позволяет пользователю выбрать путь к исходному текстовому файлу."""
    def_path = config["initial_file"]
    ans = input(f"Использовать путь по умолчанию ({def_path})? (y/n): ").strip().lower()
    if ans == "y":
        return def_path
    elif ans == "n":
        new = input("Введите полный или относительный путь к текстовому файлу: ").strip()
        if new and os.path.exists(new):
            return new
        else:
            print(f"Файл '{new}' не найден. Оставляем путь по умолчанию.")
            return def_path
    else:
        print("Неверный ввод. Использую путь по умолчанию.")
        return def_path


def generate_rsa_keys(config: dict) -> None:
    """Генерирует RSA-ключи и сохраняет их в файлы из конфига."""
    pub = config.get("public_key")
    priv = config.get("secret_key")
    if not pub or not priv:
        print("[!] В конфигурации отсутствуют пути для ключей.")
        return

    if os.path.exists(pub) or os.path.exists(priv):
        ans = input("Файлы ключей уже существуют. Перезаписать? (y/n): ").strip().lower()
        if ans != "y":
            print("Генерация отменена.")
            return

    try:
        ensure_directory_exists(pub)
        ensure_directory_exists(priv)
        private_key, public_key = RSA.generate()
        utilities.serialize_private_key(priv, private_key)
        utilities.serialize_public_key(pub, public_key)
        print(f"[+] RSA-ключи сгенерированы и сохранены:\n    Публичный: {pub}\n    Приватный: {priv}")
    except Exception as e:
        print(f"[!] Ошибка при генерации RSA-ключей: {e}")


def encrypt_text(config: dict, rsa_public_path: str) -> None:
    """Шифрует исходный текст: SM4 + RSA (гибридная схема)."""
    if not os.path.exists(rsa_public_path):
        print("[!] Публичный RSA-ключ не найден. Сначала сгенерируйте ключи (пункт 1).")
        return

    src = config.get("initial_file")
    if not src or not os.path.exists(src):
        print(f"[!] Исходный файл '{src}' не найден. Шифрование невозможно.")
        return

    try:
        public_key = utilities.deserialize_public_key(rsa_public_path)
        if public_key is None:
            print("[!] Не удалось загрузить публичный ключ.")
            return

        plaintext = utilities.read_txt_file(src)
        if not plaintext:
            print("[!] Исходный файл пуст или не удалось прочитать.")
            return

        sm4_key = SM4.generate_sm4_key()
        iv, ciphertext = SM4.sm4_encrypt(sm4_key, plaintext)
        encrypted_data = iv + ciphertext

        enc_file = config["encrypted_file"]
        ensure_directory_exists(enc_file)
        utilities.write_txt_file(encrypted_data, enc_file)

        encrypted_sm4_key = RSA.encryption(sm4_key, public_key)
        sym_file = config["symmetric_key"]
        ensure_directory_exists(sym_file)
        utilities.write_txt_file(encrypted_sm4_key, sym_file)

        print(f"\n[+] Шифрование выполнено успешно!\n    Зашифрованный текст: {enc_file}\n    Зашифрованный SM4-ключ: {sym_file}")
        print(f"SM4-ключ (16 байт): {show_hex_dump(sm4_key)}")
        print(f"IV (16 байт): {show_hex_dump(iv)}")
    except Exception as e:
        print(f"[!] Ошибка шифрования: {e}")


def decrypt_text(config: dict, rsa_private_path: str) -> None:
    """Расшифровывает текст, используя приватный RSA-ключ и SM4."""
    if not os.path.exists(rsa_private_path):
        print("[!] Приватный RSA-ключ не найден. Сначала сгенерируйте ключи (пункт 1).")
        return

    enc_file = config.get("encrypted_file")
    sym_file = config.get("symmetric_key")
    if not enc_file or not sym_file:
        print("[!] В конфигурации отсутствуют пути к зашифрованным файлам.")
        return
    if not (os.path.exists(enc_file) and os.path.exists(sym_file)):
        print("[!] Зашифрованные файлы не найдены. Сначала выполните шифрование (пункт 2).")
        return

    try:
        private_key = utilities.deserialize_private_key(rsa_private_path)
        if private_key is None:
            print("[!] Не удалось загрузить приватный ключ.")
            return

        enc_sm4_key = utilities.read_txt_file(sym_file)
        if not enc_sm4_key:
            print("[!] Файл с зашифрованным SM4-ключом пуст.")
            return

        sm4_key = RSA.decryption(enc_sm4_key, private_key)
        encrypted_data = utilities.read_txt_file(enc_file)
        if len(encrypted_data) < SM4.BLOCK_SIZE:
            print("[!] Зашифрованный файл слишком мал (отсутствует IV).")
            return

        iv = encrypted_data[:SM4.BLOCK_SIZE]
        ciphertext = encrypted_data[SM4.BLOCK_SIZE:]
        decrypted_text = SM4.sm4_decrypt(sm4_key, ciphertext, iv)

        dec_file = config["decrypted_file"]
        ensure_directory_exists(dec_file)
        utilities.write_txt_file(decrypted_text, dec_file)

        print(f"\n[+] Расшифровка выполнена успешно!\n    Расшифрованный текст: {dec_file}")
        print("\n--- Расшифрованный текст (полностью) ---")
        print(show_text(decrypted_text))
        print("\n--- SM4-ключ (расшифрованный, 16 байт) ---")
        print(show_hex_dump(sm4_key))
    except Exception as e:
        print(f"[!] Ошибка расшифровки текста: {e}")


def show_encrypted_text(config: dict) -> None:
    """Показывает полное содержимое зашифрованного файла в виде hex-дампа."""
    path = config.get("encrypted_file")
    if not path:
        print("[!] Путь к зашифрованному файлу не указан.")
        return
    print(f"\n=== Зашифрованный текст (файл: {path}) ===")
    if not os.path.exists(path):
        print("Файл не найден.")
        return
    data = utilities.read_txt_file(path)
    print(f"Размер файла: {len(data)} байт")
    print("Полный hex-дамп:")
    print(show_hex_dump(data))


def show_decrypted_text(config: dict) -> None:
    """Показывает полное содержимое расшифрованного текстового файла."""
    path = config.get("decrypted_file")
    if not path:
        print("[!] Путь к расшифрованному файлу не указан.")
        return
    print(f"\n=== Расшифрованный текст (файл: {path}) ===")
    if not os.path.exists(path):
        print("Файл не найден. Сначала выполните расшифровку.")
        return
    data = utilities.read_txt_file(path)
    print(show_text(data))


def show_keys_info(config: dict) -> None:
    """Выводит полную информацию о ключах (RSA и зашифрованном SM4-ключе)."""
    print("\n=== Информация о ключах ===")
    items = [
        ("Публичный RSA-ключ", config.get("public_key")),
        ("Приватный RSA-ключ", config.get("secret_key")),
        ("Зашифрованный SM4-ключ", config.get("symmetric_key"))
    ]
    for name, path in items:
        if not path:
            print(f"\n{name}: путь не указан")
            continue
        print(f"\n{name}: {path}")
        if not os.path.exists(path):
            print("   (файл не существует)")
            continue
        if "SM4" in name:
            data = utilities.read_txt_file(path)
            print(f"   Длина: {len(data)} байт")
            print(f"   Полный hex: {show_hex_dump(data)}")
        else:
            with open(path, 'r', encoding='utf-8') as f:
                print(f.read())


def main_menu(config: dict, initial_file: str) -> None:
    """Главное меню приложения."""
    config["initial_file"] = initial_file
    while True:
        print("\n" + "=" * 50)
        print("ГИБРИДНОЕ ШИФРОВАНИЕ (RSA + SM4)")
        print("=" * 50)
        print("1. Сгенерировать RSA-ключи")
        print("2. Зашифровать текст")
        print("3. Расшифровать текст")
        print("4. Показать зашифрованный текст (hex)")
        print("5. Показать расшифрованный текст")
        print("6. Показать ключи")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        match choice:
            case "1":
                generate_rsa_keys(config)
            case "2":
                encrypt_text(config, config.get("public_key", ""))
            case "3":
                decrypt_text(config, config.get("secret_key", ""))
            case "4":
                show_encrypted_text(config)
            case "5":
                show_decrypted_text(config)
            case "6":
                show_keys_info(config)
            case "0":
                print("До свидания!")
                sys.exit(0)
            case _:
                print("Неверный ввод, попробуйте снова.")


def main():
    settings_path = utilities.parse_arguments()
    config = load_config(settings_path)
    if not config:
        sys.exit(1)
    initial_file = choose_initial_file(config)
    main_menu(config, initial_file)


if __name__ == "__main__":
    main()