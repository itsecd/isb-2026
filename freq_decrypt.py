from collections import Counter

RUS_FREQ = "ОЕАИНТСРВЛКМДПУЯЫЬГЗБЧЙХЖШЮЦЩЭФЪ "

def read_cipher():
    with open("task2_cipher.txt", "r", encoding="utf-8") as f:
        return f.read()

def build_freq_table(text):

    counts = Counter(text)

    with open("freq_table.txt", "w", encoding="utf-8") as f:
        for ch, count in counts.most_common():

            if ch == "\n":
                continue

            name = "[SPACE]" if ch == " " else ch

            f.write(f"{name}\t{count}\n")

    return counts


def build_key(counts):

    cipher_sorted = [c for c,_ in counts.most_common() if c != "\n"]

    key = {}

    for i, c in enumerate(cipher_sorted):

        if i < len(RUS_FREQ):

            key[c] = RUS_FREQ[i]

    with open("found_key.txt","w",encoding="utf-8") as f:

        for c,p in key.items():

            left = "[SPACE]" if c==" " else c
            right = "[SPACE]" if p==" " else p

            f.write(f"{left} -> {right}\n")

    return key


def decrypt(text,key):

    result = ""

    for ch in text:

        result += key.get(ch,ch)

    return result


def main():

    cipher = read_cipher()

    counts = build_freq_table(cipher)

    key = build_key(counts)

    text = decrypt(cipher,key)

    with open("freq_decrypted.txt","w",encoding="utf-8") as f:
        f.write(text)

    print("freq_table.txt создан")
    print("found_key.txt создан")
    print("freq_decrypted.txt создан")


if __name__ == "__main__":
    main()