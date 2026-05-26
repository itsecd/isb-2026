import argparse
import sys
from file_utils import load_settings, read_file, write_file
import asymmetrical
import symmetrical

def mode_keygen(args):
    """
    Режим генерации ключей: создаёт IDEA-ключ (пользовательский или случайный),
    пару RSA, шифрует IDEA-ключ открытым RSA-ключом.
    """
    print("=== Генерация ключей гибридной системы ===")

    if args.sym_key:
        try:
            sym_key = bytes.fromhex(args.sym_key)
            if len(sym_key) != 16:
                print("Ошибка: hex-ключ должен быть длиной 32 символа (16 байт)")
                sys.exit(1)
            print(f"  Использован пользовательский ключ IDEA (128 бит): {sym_key.hex()}")
        except ValueError:
            print("Ошибка: неверный формат hex-ключа. Используйте 32 hex-символа.")
            sys.exit(1)
    else:
        sym_key = symmetrical.generate_key()
        print(f"  Сгенерирован ключ IDEA (128 бит): {sym_key.hex()}")

    private_rsa, public_rsa = asymmetrical.generate_rsa_keypair()
    print("  Сгенерирована пара RSA (2048 бит)")
    asymmetrical.save_private_key(private_rsa, args.private_key)
    asymmetrical.save_public_key(public_rsa, args.public_key)
    print(f"  Приватный RSA-ключ сохранён: {args.private_key}")
    print(f"  Публичный RSA-ключ сохранён: {args.public_key}")
    encrypted_sym = asymmetrical.encrypt_symmetric_key(public_rsa, sym_key)
    write_file(args.enc_sym_key, encrypted_sym)
    print(f"  Зашифрованный симметричный ключ сохранён: {args.enc_sym_key}")
    print("=== Генерация ключей завершена ===")

def mode_encrypt(args):
    """Режим шифрования файла: расшифровывает симметричный ключ через RSA, затем шифрует IDEA."""
    print("=== Шифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    if private_rsa is None:
        print("Ошибка: не удалось загрузить приватный ключ.")
        sys.exit(1)
    encrypted_sym = read_file(args.enc_sym_key)
    if encrypted_sym is None:
        print("Ошибка: не удалось прочитать зашифрованный симметричный ключ.")
        sys.exit(1)
    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")
    plaintext = read_file(args.input)
    if plaintext is None:
        print("Ошибка: не удалось прочитать входной файл.")
        sys.exit(1)
    encrypted_data = symmetrical.encrypt_data(sym_key, plaintext)
    if not write_file(args.output, encrypted_data):
        print("Ошибка: не удалось записать зашифрованный файл.")
        sys.exit(1)
    print(f"  Файл зашифрован: {args.output}")
    print("=== Шифрование завершено ===")

def mode_decrypt(args):
    """Режим дешифрования файла: расшифровывает симметричный ключ через RSA, затем дешифрует IDEA."""
    print("=== Дешифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    if private_rsa is None:
        print("Ошибка: не удалось загрузить приватный ключ.")
        sys.exit(1)
    encrypted_sym = read_file(args.enc_sym_key)
    if encrypted_sym is None:
        print("Ошибка: не удалось прочитать зашифрованный симметричный ключ.")
        sys.exit(1)
    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")
    encrypted_data = read_file(args.input)
    if encrypted_data is None:
        print("Ошибка: не удалось прочитать зашифрованный файл.")
        sys.exit(1)
    plaintext = symmetrical.decrypt_data(sym_key, encrypted_data)
    if not write_file(args.output, plaintext):
        print("Ошибка: не удалось записать расшифрованный файл.")
        sys.exit(1)
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
    config = load_settings(args.config)

    if args.mode == "keygen":
        enc_sym = args.enc_sym_key or config.get("keygen", {}).get("enc_sym_key")
        pub = args.public_key or config.get("keygen", {}).get("public_key")
        priv = args.private_key or config.get("keygen", {}).get("private_key")
        if not (enc_sym and pub and priv):
            print("Ошибка: для keygen укажите enc_sym_key, public_key, private_key")
            sys.exit(1)
        args.enc_sym_key = enc_sym
        args.public_key = pub
        args.private_key = priv
        mode_keygen(args)
    elif args.mode == "encrypt":
        inp = args.input or config.get("encrypt", {}).get("input_file")
        out = args.output or config.get("encrypt", {}).get("output_file")
        priv = args.private_key or config.get("encrypt", {}).get("private_key")
        enc_sym = args.enc_sym_key or config.get("encrypt", {}).get("enc_sym_key")
        if not (inp and out and priv and enc_sym):
            print("Ошибка: для encrypt укажите input, output, private_key, enc_sym_key")
            sys.exit(1)
        args.input = inp
        args.output = out
        args.private_key = priv
        args.enc_sym_key = enc_sym
        mode_encrypt(args)
    else: 
        inp = args.input or config.get("decrypt", {}).get("input_file")
        out = args.output or config.get("decrypt", {}).get("output_file")
        priv = args.private_key or config.get("decrypt", {}).get("private_key")
        enc_sym = args.enc_sym_key or config.get("decrypt", {}).get("enc_sym_key")
        if not (inp and out and priv and enc_sym):
            print("Ошибка: для decrypt укажите input, output, private_key, enc_sym_key")
            sys.exit(1)
        args.input = inp
        args.output = out
        args.private_key = priv
        args.enc_sym_key = enc_sym
        mode_decrypt(args)

if __name__ == "__main__":
    main()