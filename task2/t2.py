import os
from collections import Counter
from const import (
    INPUT_FILE, FREQ_FILE, AUTO_KEY_FILE,
    AUTO_DEC_FILE, USER_KEY_FILE, USER_DEC_FILE
)

try:
    from frequency import REFERENCE_FREQUENCIES
except ImportError:
    print("Error: frequency.py module not found")
    exit(1)


def normalize_letter(c: str) -> str:
    """Convert letter to uppercase"""
    return c.upper() if c.isalpha() else c


def read_key_file(filename: str) -> dict:
    """Read key from file"""
    mapping = {}
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ' = ' not in line:
                continue
            sym, let = line.split(' = ', 1)
            mapping[sym.strip('\'')] = let.strip()
    return mapping


def count_frequencies(text: str) -> dict:
    """Calculate frequencies of symbols in text."""
    total = len(text)
    return {ch: count / total for ch, count in Counter(text).items()}


def build_key_by_frequency(text_freq: dict, ref_freq: dict) -> dict:
    """
    Build key by frequency.
    """
    ref_items = sorted(ref_freq.items(), key=lambda x: x[1])
    ref_chars = [ch for ch, _ in ref_items]
    ref_vals = [v for _, v in ref_items]

    mapping = {}
    for ch, fq in sorted(text_freq.items(), key=lambda x: x[1], reverse=True):
        if not ref_chars:
            mapping[ch] = ch
            continue
        idx = min(range(len(ref_vals)), key=lambda i: abs(ref_vals[i] - fq))
        mapping[ch] = ref_chars[idx]
        del ref_chars[idx]
        del ref_vals[idx]

    return mapping


def decrypt(text: str, mapping: dict) -> str:
    """decrypting"""
    result = []
    for ch in text:
        if ch in '\n\r':
            result.append(ch)
        else:
            result.append(mapping.get(normalize_letter(ch), ch))
    return ''.join(result)

def write_key_to_file(key: dict,filename:str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        for sym, let in key.items():
            f.write(f"{repr(sym)} = {let}\n")


def write_decrypted_to_file(text: str, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():

    with open(INPUT_FILE, encoding='utf-8') as f:
        cipher_full = f.read()

    cipher_clean = cipher_full.replace('\n', '').replace('\r', '')
    if not cipher_clean:
        print("File is empty.")
        return

    norm_text = ''.join(normalize_letter(c) for c in cipher_clean)
    freq = count_frequencies(norm_text)

    with open(FREQ_FILE, 'w', encoding='utf-8') as f:
        for ch, fq in sorted(freq.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{repr(ch)}-{fq:.6f}\n")

    auto_key = build_key_by_frequency(freq, REFERENCE_FREQUENCIES)
    write_key_to_file(auto_key,AUTO_KEY_FILE)

    dec_auto = decrypt(cipher_full, auto_key)
    write_decrypted_to_file(dec_auto,AUTO_DEC_FILE)

    if os.path.exists(USER_KEY_FILE):
        try:
            user_key = read_key_file(USER_KEY_FILE)
            if user_key:
                dec_user = decrypt(cipher_full, user_key)
                with open(USER_DEC_FILE, 'w', encoding='utf-8') as f:
                    f.write(dec_user)
        except Exception as e:
            print(f"Error processing {USER_DEC_FILE}: {e}")


if __name__ == "__main__":
    main()
