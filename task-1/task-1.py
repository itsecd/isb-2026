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


def invert_key(m: dict[str,str]) -> dict[str, str]:

    """Инвертирует mapping: plaintext->cipher  ==>  cipher->plaintext."""

    return {v: k for k,v in m.items()}

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
    parser.add_argument("--enc", dest="enc_path", type=str, help="Путь к выходному файлу")
    parser.add_argument("--dec", dest="dec_path", type=str, help="Путь к тестовому файлу")
    args = parser.parse_args()

    in_path = Path(args.in_path)
    key_path = Path(args.key_path)
    enc_path = Path(args.enc_path)
    dec_path = Path(args.dec_path)

    text = in_path.read_text(encoding="utf-8").replace("\n", " ").upper()

    enc_map = load_key(key_path)
    dec_map = invert_key(enc_map)

    encrypted = encrypt(text, enc_map)
    decrypted = encrypt(encrypted, dec_map)

    enc_path.parent.mkdir(parents=True, exist_ok=True)
    dec_path.parent.mkdir(parents=True, exist_ok=True)
    enc_path.write_text(encrypted, encoding="utf-8")
    dec_path.write_text(decrypted, encoding="utf-8")

    if decrypted == text:
        print("OK: шифрование и расшифрование совпали (проверка пройдена).")
    else:
        print("WARN: расшифровка не совпала с исходным текстом. Проверьте key.json.")


if __name__ == "__main__":
    main()
