import sys

from ordered_set import OrderedSet


def read_text(filename: str) -> str:
    """
    Docstring for read_text

    :param filename: Input filename for reading
    :type filename: str
    :return: Text from file
    :rtype: str
    """
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    except FileExistsError:
        print(f"Failed to open file {filename}")
        exit(2)
    except PermissionError:
        print(f"Permission denied for {filename}")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)


def encode(source: str, key: str) -> str:
    """
    Docstring for encode

    :param source: Source text to encode
    :type source: str
    :param key: Secret key (English chars + digits only)
    :type key: str
    :return: Encoded text
    :rtype: str
    """
    result = source.lower()
    source_alphabet = OrderedSet(x for x in result)
    encode_alphabet = OrderedSet(sorted(key.lower()))
    print(source_alphabet)
    print(encode_alphabet)
    allowed_symbols = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ !@#$%&*0123456789\nabcdefghijklmnopqrstuvwxyz"
    )
    for i in allowed_symbols:
        if len(encode_alphabet) < len(source_alphabet):
            encode_alphabet.add(i)
    source_alphabet = list(source_alphabet)
    encode_alphabet = list(encode_alphabet)
    for i in range(len(encode_alphabet)):
        result = result.replace(source_alphabet[i], encode_alphabet[i])

    return result


def main() -> None:
    """
    Docstring for main
    """
    if len(sys.argv) != 4:
        print("Usage: python task1.py input.txt key.txt output.txt")
        exit(1)

    input_file = sys.argv[1]
    key_file = sys.argv[2]
    output_file = sys.argv[3]

    input_text = read_text(input_file)
    key = read_text(key_file)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(encode(input_text, key))
            print(f"Saved to {output_file}")
    except PermissionError:
        print(f"Permission denied for {output_file}")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)


if __name__ == "__main__":
    main()
