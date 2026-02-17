def main() -> None:
    text = ""
    with open("cod10.txt", encoding="utf-8") as f:
        text = f.read()

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


if __name__ == "__main__":
    main()
