import json
import argparse
from pathlib import Path
from collections import Counter

RUS_ORDER = " ОИЕАНТСРВМЛДЯКПЗЫЬУЧЖГХФЙЮБЦШЩЭЪ"

def freq_order(text: str) -> list[str]:

    """Символы текста по убыванию частоты (без '\\n')."""

    cnt = Counter(ch for ch in text if ch != "\n")
    return [ch for ch, _ in cnt.most_common()]

def build_initial_key(ciphertext: str, space_symbol: str | None) -> dict[str, str]:

    """Начальный ключ подстановки по частотам; space_symbol -> ' ' (если задан)."""

    order = freq_order(ciphertext)
    key: dict[str, str] = {}

    if space_symbol is not None:
        key[space_symbol] = " "
        order = [x for x in order if x != space_symbol]
        target = RUS_ORDER.replace(" ", "")
    else:
        target = RUS_ORDER

    for i, cch in enumerate(order):
        if i >= len(target):
            break
        if cch not in key:
            key[cch] = target[i]
    return key

def decrypt(ciphertext: str, key: dict[str, str]) -> str:

    """Дешифрует текст по ключу (символы вне key не меняются)."""

    return "".join(key.get(ch, ch) for ch in ciphertext)

def main():

    """либо читает готовый ключ (--use-existing-key), либо строит и сохраняет key."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", required=True)
    parser.add_argument("--out", dest="out_path", required=True)
    parser.add_argument("--key", dest="key_path", required=True)
    parser.add_argument("--space", default=None)
    parser.add_argument("--use-existing-key", action="store_true")
    args = parser.parse_args()

    ciphertext = Path(args.in_path).read_text(encoding="utf-8")
    key_path = Path(args.key_path)
    if args.use_existing_key:
        key = json.loads(key_path.read_text(encoding="utf-8"))
    else:
        key = build_initial_key(ciphertext, args.space)
        key_path.write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")

    decoded = decrypt(ciphertext, key)
    Path(args.out_path).write_text(decoded, encoding="utf-8")
    print("OK")

if __name__ == "__main__":
    main()