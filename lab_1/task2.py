def main() -> None:
    """
    Docstring for main
    """
    chars = [chr(x) for x in range(256)]
    size = 0
    text = ""
    freq = dict.fromkeys(chars, 0)
    with open("cod11.txt", "r") as f:
        text = f.read()
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


if __name__ == "__main__":
    main()
