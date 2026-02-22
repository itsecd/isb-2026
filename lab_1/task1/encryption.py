import argparse


def argument_parsing() -> list[str]:
    """
    Argument parsing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', type=str, help='path to input file')
    parser.add_argument('encryption_key', type=str, help='key to enctypt text')
    parser.add_argument('output_file_name', type=str,
                        help='path to output file')
    args = parser.parse_args()
    return [args.input_file_name, args.encryption_key, args.output_file_name]


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


def calc_letter(x: str, a: str) -> str:
    '''calculates symbol using ring algebra'''
    x_number = ord(x)-ord('А')
    a_number = ord(a)-ord('А')
    res_number = (x_number+a_number) % 33
    return chr(res_number+ord('А'))


def encrypt(text: str, key: str) -> str:
    '''function to enctypt given text using key with trivial Visiner table'''
    result = ''
    j = 0
    for letter in text:
        if letter != ' ':
            result += calc_letter(letter, key[j])
        else:
            result += ' '
        j += 1
        if j >= len(key):
            j = 0
    return result


def main():
    '''Reads input_file and enctypts it to output_file using some key'''

    # getting arguments from user
    args = argument_parsing()
    input_file = 'lab_1\\' + args[0]
    key = args[1]
    output_file = 'lab_1\\' + args[2]

    text = read_text(input_file)
    encrypted_text = encrypt(text, key)
    write_text('lab_1\\key.txt', key)
    write_text(output_file, encrypted_text)


if __name__ == '__main__':
    main()
