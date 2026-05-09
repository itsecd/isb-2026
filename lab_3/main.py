import argparse
import sys
from typing import Dict, Any
from file_utils import load_config, read_bytes, write_bytes
import asymmetrical
import symmetrical

def mode_keygen(args: argparse.Namespace) -> None:
    """Генерация ключей: IDEA, RSA, шифрование IDEA-ключа."""
    print("=== Генерация ключей гибридной системы ===")
    sym_key = symmetrical.generate_key()
    print(f"  Сгенерирован ключ IDEA (128 бит): {sym_key.hex()}")
    private_rsa, public_rsa = asymmetrical.generate_rsa_keypair()
    print("  Сгенерирована пара RSA (2048 бит)")
    asymmetrical.save_private_key(private_rsa, args.private_key)
    asymmetrical.save_public_key(public_rsa, args.public_key)
    print(f"  Приватный RSA-ключ сохранён: {args.private_key}")
    print(f"  Публичный RSA-ключ сохранён: {args.public_key}")
    encrypted_sym = asymmetrical.encrypt_symmetric_key(public_rsa, sym_key)
    write_bytes(args.enc_sym_key, encrypted_sym)
    print(f"  Зашифрованный симметричный ключ сохранён: {args.enc_sym_key}")
    print("=== Генерация ключей завершена ===")

def mode_encrypt(args: argparse.Namespace) -> None:
    """Шифрование файла: RSA-расшифровка IDEA-ключа, затем IDEA-шифрование."""
    print("=== Шифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    encrypted_sym = read_bytes(args.enc_sym_key)
    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")
    plaintext = read_bytes(args.input)
    encrypted_data = symmetrical.encrypt_data(sym_key, plaintext)
    write_bytes(args.output, encrypted_data)
    print(f"  Файл зашифрован: {args.output}")
    print("=== Шифрование завершено ===")

def mode_decrypt(args: argparse.Namespace) -> None:
    """Дешифрование файла: RSA-расшифровка IDEA-ключа, затем IDEA-дешифрование."""
    print("=== Дешифрование файла гибридной системой ===")
    private_rsa = asymmetrical.load_private_key(args.private_key)
    encrypted_sym = read_bytes(args.enc_sym_key)
    sym_key = asymmetrical.decrypt_symmetric_key(private_rsa, encrypted_sym)
    print(f"  Симметричный ключ расшифрован (длина {len(sym_key)} байт)")
    encrypted_data = read_bytes(args.input)
    plaintext = symmetrical.decrypt_data(sym_key, encrypted_data)
    write_bytes(args.output, plaintext)
    print(f"  Файл расшифрован: {args.output}")
    print("=== Дешифрование завершено ===")

def main() -> None:
    """Точка входа: разбор аргументов и вызов режима."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + IDEA")
    parser.add_argument("--config", default="settings.json", help="Путь к JSON-файлу конфигурации")
    parser.add_argument("--mode", choices=["keygen", "encrypt", "decrypt"], required=True,
                        help="Режим работы")
    parser.add_argument("--enc-sym-key", help="Путь к зашифрованному симметричному ключу")
    parser.add_argument("--public-key", help="Путь для сохранения публичного ключа (для keygen)")
    parser.add_argument("--private-key", help="Путь к/для приватного ключа")
    parser.add_argument("--input", help="Входной файл (для encrypt/decrypt)")
    parser.add_argument("--output", help="Выходной файл (для encrypt/decrypt)")

    args = parser.parse_args()

    try:
        config: Dict[str, Any] = load_config(args.config)
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        sys.exit(1)

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