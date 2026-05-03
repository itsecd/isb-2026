import modes
import os
import argparse


def args_parse() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        prog="Encrypt-decrypt data", description="Encrypt-decrypt data, generate keys"
    )
    parser.add_argument("-m", "--mode", type=int,
                        help="modes: 1(generate keys), 2(encryption data), 3(decryption data)")
    parser.add_argument("-i", "--input", type=str, help="input data file")
    parser.add_argument("-o", "--output", type=str, help="output data file")
    parser.add_argument("-s", "--sym_key", type=str,
                        help="file for symmetrical key")
    parser.add_argument("-p", "--priv_key", type=str,
                        help="file for privet key")
    return parser.parse_args()


def main() -> None:
    args = args_parse()
    match args:
