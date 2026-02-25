from consts import INPUT_FILE, DECODE_FILE, FREQENCY_FILE
from key import KEY


def decode(text: str) -> str:
    """
    Docstring for decode
    Parametrs text: str - text for decode with key
    Return decoded text: str
    """
    for i, j in KEY.items():
        text = text.replace(i, j)

    return text


def analyzer(text: str) -> str:
    """
    Docstring for analyzer
    Parametrs text: str - text for frequency analyze
    Return encoded text: str
    """
    chars = [ord(i) for i in set(text)]

    frequency = {chr(i): 0 for i in chars}

    for i in text:
        frequency[i] += 1

    for i, j in frequency.items():
        frequency[i] = j / len(text)

    frequency = {
        ch: fr
        for ch, fr in sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    }

    with open(FREQENCY_FILE, "w", encoding="utf-8") as f:
        for ch, fr in frequency.items():
            f.write(ch + " " + str(fr) + "\n")


def main() -> None:
    """
    Main function.
    """
    text = ""
    with open(INPUT_FILE, encoding="utf-8") as f:
        text = f.read()
    text = decode(text)
    print(text)

    with open(DECODE_FILE, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
