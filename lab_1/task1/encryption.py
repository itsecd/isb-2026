import argparse

'''
Instruction for using this file:
    python input_file_name encryption_key encrypted_file_name decrypted_file_name
'''


def argument_parsing() -> list[str]:
    """
    Argument parsing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name', type=str, help='path to input file')
    parser.add_argument('encryption_key', type=str, help='key to enctypt text')
    parser.add_argument('encrypted_file_name', type=str,
                        help='path to encrypted file')
    parser.add_argument('dectypted_file_name', type=str,
                        help='path to encrypted file')
    args = parser.parse_args()
    return [args.input_file_name, args.encryption_key, args.encrypted_file_name, args.dectypted_file_name]


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


def calc_letter(x: str, a: str, encrypt: bool) -> str:
    '''calculates symbol using ring algebra'''
    x_number = ord(x)-ord('А')
    a_number = ord(a)-ord('А')
    if encrypt:
        res_number = (x_number+a_number) % 33
    else:
        res_number = (x_number-a_number) % 33
    return chr(res_number+ord('А'))


def text_transform(text: str, key: str, encrypt: bool) -> str:
    '''function to enctypt given text using key with trivial Visiner table'''
    result = ''
    j = 0
    for letter in text:
        if letter != ' ':
            result += calc_letter(letter, key[j], encrypt)
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
    input_file = args[0]
    key_file = args[1]
    encrypted_file = args[2]
    decrypted_file = args[3]

    text = read_text(input_file)
    key = read_text(key_file)

    # text encryption
    encrypted_text = text_transform(text, key, encrypt=True)
    write_text(encrypted_file, encrypted_text)

    # text decryption
    decrypted_text = text_transform(encrypted_text, key, encrypt=False)
    write_text(decrypted_file, decrypted_text)


if __name__ == '__main__':
    main()


# python lab_1\task1\encryption.py lab_1\task1\task1_text.txt lab_1\task1\key.txt lab_1\task1\task1_enctypted.txt lab_1\task1\task1_dectypted.txt
