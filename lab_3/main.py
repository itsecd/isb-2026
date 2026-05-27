import argparse
import sys
from file_utils import read_json, read_file, write_file
import asymmetrical
import symmetrical

def mode_keygen(args):
    """Генерация ключей: IDEA (пользовательский или случайный), RSA, шифрование IDEA-ключа."""
    print("=== Генерация ключей гибридной системы ===")

    if args.sym_key:
        try:
            sym_key = bytes.fromhex(args.sym_key)
            if len(sym_key) != 16:
                raise ValueError("hex-ключ должен быть длиной 32 символа (16 байт)")
            print(f"  Использован пользовательский ключ IDEA: {sym_key.hex()}")
        except ValueError as e:
            raise ValueError(f"Неверный формат hex-ключа: {e}")
    else:
        sym_key = symmetrical.generate_key()
        print(f"  Сгенерирован ключ IDEA: {sym_key.hex()}")

    private_rsa, public_rsa = asymmetrical.generate_rsa_keypair()
    print("  Сгенерирована пара RSA (2048 бит)")
    asymmetrical.save_private_key(private_rsa, args.private_key)
    asymmetrical.save_public_key(public_rsa, args.public_key)
    print(f"  Приватный RSA-ключ сохранён: {args.private_key}")
    print(f"  Публичный RSA-ключ сохранён: {args.public_key}")

    encrypted_sym = asymmetrical.encrypt_symmetric_key(public_rsa, sym_key)
    if not write_file(args.enc_sym_key, encrypted_sym):
        raise RuntimeError("Не удалось сохранить зашифрованный симметричный ключ")
    print(f"  Зашифрованный симметричный ключ сохранён: {args.enc_sym_key}")
    print("=== Генерация ключей завершена ===")

def mode_encrypt(args):
    """Шифрование файла: расшифровка IDEA-ключа через RSA, затем IDEA-шифрование."""
    print("=== Шифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    if private_rsa is None:
        raise RuntimeError("Не удалось загрузить приватный ключ")

    encrypted_sym = read_file(args.enc_sym_key)
    if encrypted_sym is None:
        raise RuntimeError("Не удалось прочитать зашифрованный симметричный ключ")

    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")

    plaintext = read_file(args.input)
    if plaintext is None:
        raise RuntimeError("Не удалось прочитать входной файл")

    encrypted_data = symmetrical.encrypt_data(sym_key, plaintext)
    if not write_file(args.output, encrypted_data):
        raise RuntimeError("Не удалось записать зашифрованный файл")

    print(f"  Файл зашифрован: {args.output}")
    print("=== Шифрование завершено ===")

def mode_decrypt(args):
    """Дешифрование файла: расшифровка IDEA-ключа через RSA, затем IDEA-дешифрование."""
    print("=== Дешифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    if private_rsa is None:
        raise RuntimeError("Не удалось загрузить приватный ключ")

    encrypted_sym = read_file(args.enc_sym_key)
    if encrypted_sym is None:
        raise RuntimeError("Не удалось прочитать зашифрованный симметричный ключ")

    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")

    encrypted_data = read_file(args.input)
    if encrypted_data is None:
        raise RuntimeError("Не удалось прочитать зашифрованный файл")

    plaintext = symmetrical.decrypt_data(sym_key, encrypted_data)
    if not write_file(args.output, plaintext):
        raise RuntimeError("Не удалось записать расшифрованный файл")

    print(f"  Файл расшифрован: {args.output}")
    print("=== Дешифрование завершено ===")

def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + IDEA")
    parser.add_argument("--config", default="settings.json", help="Путь к JSON-файлу конфигурации")
    parser.add_argument("--mode", choices=["keygen", "encrypt", "decrypt"], required=True,
                        help="Режим работы")
    parser.add_argument("--sym-key", help="Пользовательский ключ IDEA в hex (32 символа). Если не указан, генерируется случайный.")
    parser.add_argument("--enc-sym-key", help="Путь к зашифрованному симметричному ключу")
    parser.add_argument("--public-key", help="Путь для сохранения публичного ключа (для keygen)")
    parser.add_argument("--private-key", help="Путь к/для приватного ключа")
    parser.add_argument("--input", help="Входной файл (для encrypt/decrypt)")
    parser.add_argument("--output", help="Выходной файл (для encrypt/decrypt)")

    args = parser.parse_args()
    config = read_json(args.config)
    if config is None:
        print(f"Ошибка: не удалось загрузить настройки из файла {args.config}")
        sys.exit(1)

    try:
        match args.mode:
            case "keygen":
                args.enc_sym_key = args.enc_sym_key or config.get("keygen", {}).get("enc_sym_key")
                args.public_key = args.public_key or config.get("keygen", {}).get("public_key")
                args.private_key = args.private_key or config.get("keygen", {}).get("private_key")
                if not (args.enc_sym_key and args.public_key and args.private_key):
                    raise ValueError("Для keygen укажите enc_sym_key, public_key, private_key")
                mode_keygen(args)
            case "encrypt":
                args.input = args.input or config.get("encrypt", {}).get("input_file")
                args.output = args.output or config.get("encrypt", {}).get("output_file")
                args.private_key = args.private_key or config.get("encrypt", {}).get("private_key")
                args.enc_sym_key = args.enc_sym_key or config.get("encrypt", {}).get("enc_sym_key")
                if not (args.input and args.output and args.private_key and args.enc_sym_key):
                    raise ValueError("Для encrypt укажите input, output, private_key, enc_sym_key")
                mode_encrypt(args)
            case "decrypt":
                args.input = args.input or config.get("decrypt", {}).get("input_file")
                args.output = args.output or config.get("decrypt", {}).get("output_file")
                args.private_key = args.private_key or config.get("decrypt", {}).get("private_key")
                args.enc_sym_key = args.enc_sym_key or config.get("decrypt", {}).get("enc_sym_key")
                if not (args.input and args.output and args.private_key and args.enc_sym_key):
                    raise ValueError("Для decrypt укажите input, output, private_key, enc_sym_key")
                mode_decrypt(args)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()