import json
import os.path
from collections import Counter


def load_json(path: str) -> dict:
    """
    Load key from JSON

    :param path: Stored key path
    :return: Key
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(path: str, data: dict) -> None:
    """
    Save key to JSON

    :param path: Path to save key to
    :param data: Key
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def generate_key(text: str, reference_frequencies: dict) -> dict:
    """
    Generating key for decryption based on frequencies

    :param text: Text to analyze frequency in
    :param reference_frequencies: Standard frequencies in russian language
    :return: Key
    """
    # Count how often each char appears
    text_count = Counter(text)
    # Sort chars
    text_sorted = [char for char, count in text_count.most_common()]
    key_map = {}
    # Create a dictionary using comparison with reference
    for text_char, reference_char in zip(text_sorted, reference_frequencies):
        key_map[text_char] = reference_char
    return key_map


def decrypt_text(text: str, key_map: dict) -> str:
    """
    Decrypting text using dictionary

    :param text: Text to decrypt
    :param key_map: Dictionary for decryption
    :return: Decrypted text
    """
    result = ""
    for char in text:
        result += key_map.get(char, char)
    return result


def main() -> None:
    """
    Main function
    """
    data_dir = 'data'
    reference_frequencies_path = 'frequencies.json'
    input_path = os.path.join(data_dir, 'cod8.txt')
    key_path = os.path.join(data_dir, 'key.json')
    output_path = os.path.join(data_dir, 'decrypt.txt')

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Input file not found at: {input_path}")
        return

    if not os.path.exists(reference_frequencies_path):
        print(f"No reference frequencies file at: {reference_frequencies_path}")
        return

    # Create key only if it's not existing
    if not os.path.exists(key_path):
        print("Creating new key file")
        reference_frequencies = load_json(reference_frequencies_path)
        key_map = generate_key(input_text, reference_frequencies)
        save_json(key_path, key_map)
        print(f"Key saved at: {key_path} now open it and redact it")
    # If key is present, decrypt using it
    else:
        print(f"Using key to decrypt at: {key_path}")
        key_map = load_json(key_path)

    decrypted_text = decrypt_text(input_text, key_map)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

    print(f"Decrypted text saved at: {output_path} \n Decrypted text:\n")
    print(decrypted_text)


if __name__ == "__main__":
    main()
