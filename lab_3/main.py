import modes
import os
import argparse
import rw

JSON_file = "path.json"


def args_parse() -> argparse.Namespace:
    """Парсит аргументы командной строки.
    возвращает аргументы командной строки"""
    parser = argparse.ArgumentParser(
        prog="Encrypt-decrypt data", description="Encrypt-decrypt data, generate keys"
    )
    parser.add_argument('-j', '--path', default=JSON_file,
                        type=str, help="Use your json")

    parser.add_argument("-m", "--mode", type=int,
                        help="modes: 1(generate keys), 2(encryption data), 3(decryption data), 4(generate keys and encryption data)")
    parser.add_argument("-i", "--input", type=str, help="input data file")
    parser.add_argument("-o", "--output", type=str, help="output data file")
    parser.add_argument("-s", "--sym_key", type=str,
                        help="file for symmetrical key")
    parser.add_argument("-p", "--priv_key", type=str,
                        help="file for privet key")
    return parser.parse_args()


def main() -> None:
    args = args_parse()
    path = rw.open_json(args.path)
    private_key_path = path["private_key"]
    sym_key_path = path["sym_key"]
    e_path = path["encrypted_file"]
    d_path = path["decrypted_file"]
    match args.mode:
        case 1:
            if (args.sym_key):
                sym_key_path = args.sym_key
            if (args.priv_key):
                private_key_path = args.priv_key
            modes.generate_key_mode(sym_key_path, private_key_path)
        case 2:
            if (args.sym_key):
                sym_key_path = args.sym_key
            if (args.priv_key):
                private_key_path = args.priv_key
            if (args.input):
                d_path = args.input
            if (args.output):
                e_path = args.output
            modes.encrypt_data_mode(
                d_path, e_path, sym_key_path, private_key_path)
        case 3:
            if (args.sym_key):
                sym_key_path = args.sym_key
            if (args.priv_key):
                private_key_path = args.priv_key
            if (args.input):
                e_path = args.input
            if (args.output):
                d_path = args.output
            modes.decrypt_data_mode(
                e_path, d_path, sym_key_path, private_key_path)
        case 4:
            if (args.sym_key):
                sym_key_path = args.sym_key
            if (args.priv_key):
                private_key_path = args.priv_key
            if (args.input):
                d_path = args.input
            if (args.output):
                e_path = args.output
            modes.encrypt_data_all_mode(
                sym_key_path, private_key_path, d_path, e_path)


if __name__ == "__main__":
    main()