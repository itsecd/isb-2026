import argparse


def argument_parsing() -> list[str]:
    """
    Разделение аргументов, введённых пользователем в консоли
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', type=str, help='path to input file')
    parser.add_argument('encryption_key', type=str, help='key to enctypt text')
    parser.add_argument('output_file_name', type=str,
                        help='path to output file')
    args = parser.parse_args()
    return [args.input_file_name, args.encryption_key, args.output_file_name]


def read_text(input_file: str) -> str:
    with open(input_file, 'r', encoding='utf-8') as file:
        return file.read()


def main():
    '''Reads input_file and enctypts it to output_file using some key'''
    args = argument_parsing()
    input_file = args[0]
    key = args[1]
    output_file = args[2]

    text = read_text(input_file)
    print(text)


if __name__ == '__main__':
    main()
