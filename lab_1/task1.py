import sys


def read_text(filename: str) -> str:
    """
    Docstring for read_text

    :param filename: Input filename for reading
    :type filename: str
    :return: Text from file
    :rtype: str
    """
    try:
        with open(filename) as f:
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
        with open(output_file, "w") as f:
            f.write(encode(input_text, key))
    except PermissionError:
        print(f"Permission denied for {output_file}")
        exit(2)
    except Exception as e:
        print(e)
        exit(2)


if __name__ == "__main__":
    main()
