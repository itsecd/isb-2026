import os
from collections import Counter

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


def main():
    input_file = "cod16.txt"
    freq_file = "frequency_in_text.txt"
    auto_key_file = "key.txt"
    auto_dec_file = "decrypted.txt"
    user_key_file = "key_2.txt"
    user_dec_file = "decrypted_2.txt"

    with open(input_file, encoding='utf-8') as f:
        cipher_full = f.read()

    cipher_clean = cipher_full.replace('\n', '').replace('\r', '')
    if not cipher_clean:
        print("File is empty.")
        return

    norm_text = ''.join(normalize_letter(c) for c in cipher_clean)
    freq = count_frequencies(norm_text)

    with open(freq_file, 'w', encoding='utf-8') as f:
        for ch, fq in sorted(freq.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{repr(ch)}-{fq:.6f}\n")

    auto_key = build_key_by_frequency(freq, REFERENCE_FREQUENCIES)

    with open(auto_key_file, 'w', encoding='utf-8') as f:
        for sym, let in auto_key.items():
            f.write(f"{repr(sym)} = {let}\n")

    dec_auto = decrypt(cipher_full, auto_key)
    with open(auto_dec_file, 'w', encoding='utf-8') as f:
        f.write(dec_auto)

    if os.path.exists(user_key_file):
        try:
            user_key = read_key_file(user_key_file)
            if user_key:
                dec_user = decrypt(cipher_full, user_key)
                with open(user_dec_file, 'w', encoding='utf-8') as f:
                    f.write(dec_user)
        except Exception as e:
            print(f"Error processing {user_key_file}: {e}")


if __name__ == "__main__":

    main()
