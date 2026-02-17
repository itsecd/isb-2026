def decode(text: str) -> str:
    """
    Decoding text
    """
    dictionary = {"Y": " ", "Ё": "о", "К":"е", "Я":"и", "s": "л", "Й":"т",
                  "U":"н", "Д":"к", "i":"ь", "ю":"р", "7":"п", "Q":"с",
                  "И":"в", "R":"а", "г":"б", "@":"з", "Ж":"я", "О":"ш",
                  "Т":"ж", "F":"э", "J":"й", "G":"ч", "Р":"ю", "1":"ы",
                  "у":"ъ", "%":"д", "3":"м", "=":"г", "Z":"ц", "Х":"х", "N":"ф", "П":"щ", "<":"у"}

    for i, j in dictionary.items():
        text = text.replace(i, j)

    return text


def analyzer(text: str) -> str:
    """
    Get frequency of chars 
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

    with open("freq.txt", "w", encoding="utf-8") as f:
        for ch, fr in frequency.items():
            f.write(ch + " " + str(fr) + "\n")


def main() -> None:
    """
    Main function.
    """
    text = ""
    with open("cod10.txt", encoding="utf-8") as f:
        text = f.read()
    text = decode(text)
    print(text)

    with open("decode.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
