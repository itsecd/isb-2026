import collections
import task2_alf


def get_sorted_frequencies(text: str) -> list:
    clean_text: str = text.replace("\n", "").replace("\r", "")
    char_counts: collections.Counter = collections.Counter(clean_text)
    total_chars: int = len(clean_text)
    return sorted(char_counts.items(), key=lambda x: x[1], reverse=True)


def main() -> None:
    with open(task2_alf.INPUT_FILE, "r", encoding="utf-8") as file:
        ciphertext: str = file.read()

    clean_text: str = ciphertext.replace("\n", "").replace("\r", "")
    char_counts: collections.Counter = collections.Counter(clean_text)
    total_chars: int = len(clean_text)

    sorted_cipher_chars: list = get_sorted_frequencies(ciphertext)
    sorted_cipher_chars: list = sorted(
        char_counts.items(), key=lambda x: x[1], reverse=True
    )
    total_chars: int = sum(count for char, count in sorted_cipher_chars)

    with open(task2_alf.FREQ_FILE, "w", encoding="utf-8") as file:
        for char, count in sorted_cipher_chars:
            frequency = (count / total_chars) * 100
            file.write(f"'{char}': {count} ({frequency:.2f}%)\n")

    decryption_key = {}

    with open(task2_alf.KEY_FILE, "w", encoding="utf-8") as file:
        for char in sorted(decryption_key.keys()):
            file.write(f"{char} | {decryption_key[char]}\n")


if __name__ == "__main__":
    main()