def compute_letter_frequencies(text: str) -> None:
    """
    Подсчет частоты символов и запись в файл 'freq_output.txt' без 
    спецсимволов.
    """
    valid_chars = [
        "Z", "9", "E", "n", "I", "A", "C", "F", "!", "W", "h", "P", "U",
        "V", "x", "O", "K", "S", "-", "M", "=", "B", "J", "t", "L", " ",
        "$", "3", "R", "G", "Q", "8", ">", "Y", "d"
    ]

    freq_dict = {ch: 0 for ch in valid_chars}
    total_chars = 0

    for ch in text:
        if ch in freq_dict:
            freq_dict[ch] += 1
            total_chars += 1

    sorted_freq = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)

    with open("freq_output.txt", "w", encoding="utf-8") as f:
        for ch, count in sorted_freq:
            if count > 0:
                f.write(f"{ch} {count / total_chars:.10f}\n")


def read_key_file(file_path: str) -> dict:
    """
    Считываем ключи вида символ=замена из файла key2.txt.
    Значение оставляем как есть (может быть пробел).
    """
    key_map = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or "=" not in line:
                continue
            src, dst = line.rsplit("=", 1)
            src = src.strip()
            key_map[src] = dst

    return key_map


def decode_text(text: str, key_map: dict) -> str:
    """
    Дешифровка текста по таблице ключей.
    """
    decoded_chars = [key_map.get(ch, ch) for ch in text]
    decoded_text = "".join(decoded_chars)

    return decoded_text


def main() -> None:
    """Основная функция: чтение, подсчет частот и дешифровка текста."""
    with open("cod12.txt", "r", encoding="utf-8") as f:
        encrypted_text = f.read()

    compute_letter_frequencies(encrypted_text)

    key_map = read_key_file("key2.txt")
    decoded_text = decode_text(encrypted_text, key_map)

    with open("decoded_output.txt", "w", encoding="utf-8") as f:
        f.write(decoded_text)


if __name__ == "__main__":
    main()
