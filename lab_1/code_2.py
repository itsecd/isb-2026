import os

os.chdir(r"C:\Users\Lenovo\Desktop\прога\четвёртый семестр\ОИБ\lab1+2\isb-2026\lab_1\part 2")

from consts_2 import (
    FREQUENCY_ORDER
)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def count_frequencies(text):
    counts = {}
    total = len(text)

    for symb in text:
        counts[symb] = counts.get(symb, 0) + 1

    freq = {}
    for symb, count in counts.items():
        freq[symb] = count / total
    return freq

def sort_symbs(freq):
    symbs = list(freq.keys())
    for i in range(len(symbs)):
        for j in range(i + 1, len(symbs)):
            if freq[symbs[i]] < freq[symbs[j]]:
                symbs[i], symbs[j] = symbs[j], symbs[i]
    return symbs

def save_frequencies(freq, filename):
    total = 0
    for value in freq.values():
        total += value

    symbs = sort_symbs(freq)

    with open(filename, "w", encoding="utf-8") as file:
        for symb in symbs:
            relative = freq[symb] / total
            file.write(symb + " : " + str(relative) + "\n")

def in_key(filename):
    key = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(" = ")
                if len(parts) == 2:
                    key[parts[0]] = parts[1]
    except OSError:
        return None

    return key

def build_key(sorted_symbs):
    key = {}
    for i in range(len(sorted_symbs)):
        if i < len(FREQUENCY_ORDER):
            key[sorted_symbs[i]] = FREQUENCY_ORDER[i]
    return key

def save_key(key, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for symb in key:
            file.write(symb + " = " + key[symb] + "\n")

def decrypt(text, key):
    result = ""
    for char in text:
        if char in key:
            result += key[char]
        else:
            result += char
    return result

def main():
    try:
        orig_text = read_file("original_text_2.txt")
        orig_text = orig_text.replace("-", " ")
        freq = count_frequencies(orig_text)
        save_frequencies(freq, "frequency_table.txt")

        key = in_key("key_2.txt")
        if key is None:
            sorted_symbs = sort_symbs(freq)
            key = build_key(sorted_symbs)
            save_key(key, "key_2.txt")
            print("A new key has been created.")
        else:
            print("The key is downloaded from a file.")

        decrypted_text = decrypt(orig_text, key)
        write_file("decrypted_text_2.txt", decrypted_text)

    except Exception as e:
        print(f"There is a mistake: {e}")

if __name__ == "__main__":
    main()