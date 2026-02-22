import argparse


def argument_parsing() -> list[str]:
    """
    Argument parsing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', type=str, help='path to input file')
    parser.add_argument('bijection_file', type=str, help='key to enctypt text')
    parser.add_argument('transform_result_file', type=str,
                        help='key to enctypt text')

    args = parser.parse_args()
    return [args.input_file_name, args.bijection_file, args.transform_result_file]


def read_text(input_file: str) -> str:
    '''Reading text from file'''
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError('No such file exist')


def write_text(output_file: str, text: str) -> None:
    '''Writing results to file'''
    with open(output_file, 'w+', encoding='utf-8') as output:
        output.write(text)


def bijection_transform(text: str, bij_dict: dict) -> str:
    result = ''
    for letter in text:
        if letter == '\n':
            result += '\n'
        else:
            result += bij_dict[letter]
    return result


def read_bijection(bijection_path: str) -> dict:
    try:
        with open(bijection_path, 'r', encoding='utf-8') as file:
            d = dict()
            for string in file.readlines():
                key, value = string.replace(' \n', '').split('\t')
                d[key] = value
            return d

    except FileNotFoundError:
        raise FileNotFoundError('No such file exist')


def main():
    args = argument_parsing()
    input_path = args[0]
    bijection_path = args[1]
    result_path = args[2]
    text = read_text(input_path)
    bijection = read_bijection(bijection_path)

    result = bijection_transform(text, bijection)
    print(result)
    write_text(result_path, result)


if __name__ == '__main__':
    main()
