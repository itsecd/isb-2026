import argparse


def argument_parsing() -> list[str]:
    """
    Argument parsing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', type=str, help='path to input file')
    parser.add_argument('output_file_name', type=str,
                        help='path to output file')
    args = parser.parse_args()
    return [args.input_file_name, args.output_file_name]


def read_text(input_file: str) -> str:
    '''Reading text from file'''
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError('No such file exist')


def calc_frequencies(text: str) -> dict:
    d = dict()
    for letter in text:
        if letter not in d:
            d[letter] = 1
        else:
            d[letter] += 1

    text_len = len(text)
    for key in d:
        d[key] = d[key]/text_len
    return d


def write_dict(output_file: str, d: dict) -> None:
    '''Writing results to file'''
    with open(output_file, 'w+', encoding='utf-8') as output:
        for key in d:
            output.write(key + ':\t' + str(d[key])+'\n')


def main():
    args = argument_parsing()
    text_file = 'lab_1\\'+args[0]
    result_file = 'lab_1\\'+args[1]
    text = read_text(text_file)
    d = calc_frequencies(text)
    write_dict(result_file, d)


if __name__ == '__main__':
    main()
