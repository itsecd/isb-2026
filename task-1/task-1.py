import json
import argparse
from pathlib import Path

ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


def load_key(key_path: Path) -> dict[str,str]:

    """Читает key.json и возвращает mapping plaintext->cipher. 
    Проверяет корректность алфавита и перестановки."""

    data=json.loads(key_path.read_text(encoding="utf-8"))
    alphabet=data["alphabet"]
    cipher_alphabet=data["cipher_alphabet"]

    if alphabet != ALPHABET:
        raise ValueError("Ошибка: alphabet в key.json не совпадает с алфавитом задания")
    if len(cipher_alphabet) != len(alphabet):
        raise ValueError("Ошибка: cipher_alphabet должен иметь ту же длину, что и alphabet")
    if sorted(cipher_alphabet) != sorted(alphabet):
        raise ValueError("Ошибка: cipher_alphabet не является корректной перестановкой alphabet")
    
    return dict(zip(alphabet,cipher_alphabet))


def encrypt(text:str, key_map: dict[str,str]) ->str:

    """Шифрует текст простой подстановкой: символы из key_map заменяются, остальные сохраняются."""

    result_chars = []
    for ch in text:
        if ch in key_map:
            result_chars.append(key_map[ch])
        else:
            result_chars.append(ch)
    return "".join(result_chars)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", type=str, help="Путь к файлу открытого текста")
    parser.add_argument("--key", dest="key_path", type=str, help="Путь к файлу key.json")
    parser.add_argument("--out", dest="out_path", type=str, help="Путь к выходному файлу")
    args = parser.parse_args()

    in_path = Path(args.in_path)
    key_path = Path(args.key_path)
    out_path = Path(args.out_path)

    text = in_path.read_text(encoding="utf-8").replace("\n", " ").upper()
    key_map = load_key(key_path)
    cipher = encrypt(text, key_map)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(cipher, encoding="utf-8")

    print(f"Готово: шифртекст записан в файл: {out_path}")


if __name__ == "__main__":
    main()
