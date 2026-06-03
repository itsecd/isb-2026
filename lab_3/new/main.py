import argparse
from settings_loader import load_config
from core.hybrid import generate_keys, encrypt_file, decrypt_file


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", default="settings.json")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", action="store_true")
    group.add_argument("-enc", action="store_true")
    group.add_argument("-dec", action="store_true")

    args = parser.parse_args()
    cfg = load_config(args.config)

    match True:
        case _ if args.gen:
            generate_keys(
                cfg["encrypted_key_file"],
                cfg["public_key_file"],
                cfg["private_key_file"]
            )

        case _ if args.enc:
            encrypt_file(
                cfg["input_file"],
                cfg["private_key_file"],
                cfg["encrypted_key_file"],
                cfg["encrypted_file"]
            )

        case _ if args.dec:
            decrypt_file(
                cfg["encrypted_file"],
                cfg["private_key_file"],
                cfg["encrypted_key_file"],
                cfg["decrypted_file"]
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
