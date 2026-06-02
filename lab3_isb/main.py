import argparse
import json
import scenario1
import scenario2
import scenario3



def load_config(config_path: str) -> dict:
    """
    Загрузка конфигурации из JSON-файла.
    :param config_path: путь к JSON-файлу с конфигурацией
    :return: словарь с параметрами конфигурации
    """

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {config_path}") from e

def argparsing() -> argparse.Namespace:
    """
    Парсер аргументов командной строки.
    :return: объект с аргументами командной строки
    """

    parser = argparse.ArgumentParser(description="Hybrid cryptosystem")
    subparsers = parser.add_subparsers(dest="scenario", required=True)
    gen_parser = subparsers.add_parser("gen", help="Generate keys")
    gen_parser.add_argument("--config", type=str, default="config.json", help="Path to config file")
    
    enc_parser = subparsers.add_parser("enc", help="Encrypt file")
    enc_parser.add_argument("--config", type=str, default="config.json", help="Path to config file")

    dec_parser = subparsers.add_parser("dec", help="Decrypt file")
    dec_parser.add_argument("--config", type=str, default="config.json", help="Path to config file")

    return parser.parse_args()

   

def main():
    args = argparsing()
    config = load_config(args.config)
    match args.scenario:
        case "gen":
            scenario1.run_scenario1(config["encrypted_aes_key"], config["public_key"], config["private_key"], config["aes_key_size"])
        case "enc":
            scenario2.run_scenario2(config["input_text"], config["private_key"], config["encrypted_aes_key"], config["encrypted_text"])
        case "dec":
            scenario3.run_scenario3(config["encrypted_text"], config["private_key"], config["encrypted_aes_key"], config["decrypted_text"])
        case _:
            raise ValueError("Unknown scenario")



if __name__ == "__main__":
    main()
