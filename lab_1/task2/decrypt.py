import argparse
from const import *
from file_work import *
from key import KEY


def get_freq(text: str) -> dict[str, float]:
    """Функция подсчёта частот"""
    symbols = set(text.strip())
    freq = {}
    
    for el in symbols:
        if el != "\n":
            freq[el] = round(text.count(el) / len(text), 6)

    return dict(sorted(freq.items(), key=lambda it: it[1], reverse=True))


def save_freq(filename: str, freq_dict: dict[str, float]) -> None:
    """Данная функция сохраняет частоты в файл"""
    with open(filename, "w", encoding="utf-8") as f:
        for (key, val) in freq_dict.items():
            f.writelines(key + " : " + str(val) + "\n")


def input_parse() -> argparse.Namespace:
    """Данная функция получает аргументы из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', help='путь к входному файлу с зашифрованным текстом')
    parser.add_argument('--output', '-o', help='путь для сохранения дешифрованного текста')
    
    return parser.parse_args()


def decrypt(text: str, filename: str) -> None:
    dec_t = ""
    
    for el in text:
        if el in KEY:
            dec_t += KEY[el]
        else:            
            dec_t += el
    
    write_file(filename, dec_t)


def main() -> None:
    args = input_parse()
    enc_path, dec_path = args.input, args.output

    enc_text = read_file(enc_path)
    freq = get_freq(enc_text)
    save_freq(FREQ_FILE, freq)
    decrypt(enc_text, dec_path)


if __name__ == "__main__":
    main() 