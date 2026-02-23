import json


def get_freq_file(text: str) -> None:
    """
    Docstring for get_freq_file
    return table frequency of chars to file
    """
    chars = [chr(x) for x in range(256)]
    size = 0
    freq = dict.fromkeys(chars, 0)
    for i in text:
        freq[i] += 1
        size += 1
    freq = {
        k: v
        for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)
        if v != 0
    }

    with open("freq_text.txt", "w") as f:
        for ch, fr in freq.items():
            f.write(ch + " " + str(fr / size) + "\n")


def decode_text(text: str) -> None:
    """
    Docstring for decode_text

    :param text: Encoded text to decode
    :type text: str
    """
    replace_table = json.load(open("key.txt", "r", encoding="utf-8"))

    for i, j in replace_table.items():
        text = text.replace(i, j)

    print(text)
    with open("decode.txt", "w", encoding="utf-8") as f:
        f.write(text)


def main() -> None:
    """
    Docstring for main
    """
    text = ""
    with open("cod11.txt", "r") as f:
        text = f.read()

    get_freq_file(text)
    decode_text(text)


if __name__ == "__main__":
    main()
