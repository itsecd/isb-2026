import argparse


def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as rfile:
            return rfile.read()
    except FileNotFoundError as e:
        raise


def write_file(file_path: str, text: str) -> str:
    try:
        with open(file_path, "w", encoding="utf-8") as wfile:
            return wfile.write(text)
    except FileNotFoundError as e:
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read_file", "-rf", type=str, required=True)
    parser.add_argument("--write_file", "-wf", type=str, required=False)
    parser.add_argument("--key_file", "-kf", type=str, required=False)
    return parser.parse_args()


def get_frequency_analysis(text: str) -> str:
    counter = {}
    for ch in text:
        counter[ch] = counter.get(ch, 0) + 1

    sorted_table = sorted(counter.items(), key=lambda item: item[1], reverse=True)
    return "".join(ch for ch, _ in sorted_table)


def create_substitution_table(cipher_order: str) -> dict:
    alphabet = " ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"
    table = {}
    for i, ch in enumerate(cipher_order):
        if i < len(alphabet):
            table[ch] = alphabet[i]
    return table


def decrypting_text(text: str, table: dict) -> str:
    return "".join(table.get(ch, ch) for ch in text)




def save_key(table: dict, path: str):
    """Сохраняет ключ подстановки в файл"""
    with open(path, "w", encoding="utf-8") as f:
        for cipher_ch, plain_ch in table.items():
            f.write(f"{cipher_ch} -> {plain_ch}\n")


def main() -> None:
    args = parse_args()
    text = read_file(args.read_file).replace("\n", "")

    # Автоматическая подстановка по частотам
    cipher_order = get_frequency_analysis(text)
    table = create_substitution_table(cipher_order)

    print("Автоматическая подстановка (первые 500 символов):")
    preview = decrypting_text(text, table)
    print(preview[:500])

    # Возможность вручную корректировать


    # Итоговый расшифрованный текст
    result = decrypting_text(text, table)
    print("\nИТОГ (первые 1000 символов):")
    print(result[:1000])

    # Сохраняем ключ, если путь указан
    if args.key_file:
        save_key(table, args.key_file)

    # Сохраняем расшифрованный текст
    if args.write_file:
        write_file(args.write_file, result)


if __name__ == "__main__":
    main()