import argparse
from decipher_key import key


def read_file (file_name: str) -> str:
    """
    читает текст из файла
    """
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()
        return text


def get_periodicity (text: str) -> str:
    """
    считает частоты встречаемости символов в тексте
    """
    text = text.upper()
    n = len(text)

    result = []
    completed_characters = []

    for character in text:
        if character not in completed_characters:
            count = 0
            for i in text:
                if i == character:
                    count += 1
            periodicity = round(count / n, 6)
            
            result.append((character, periodicity))
            completed_characters.append(character)

    result.sort(key = lambda x: x[1], reverse = True)

    final_table = ""

    for character,periodicity in result:
        final_table += f"{character} : {periodicity}\n" 
    
    return final_table


def periodicity_analysis (text: str, key: dict) -> str:
    """
    заменяет символы в тексте с помощью ключа
    """
    text = text.upper()
    result = ""

    for character in text:
        if character in key:
            result += key[character]
        else:
            result += character
    
    return result


def write_file (text:str, output_file: str) -> None:
    """
    записывает текст в файл
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--input_file_name', type=str, default='cod16.txt', help='name of input file')
    parser.add_argument("-p", '--periodicity_file_name', type=str, default='periodicity.txt', help='name of periodicity file')
    parser.add_argument("-o", '--output_file_name', type=str, default='result_of_decipher.txt', help='name of output file')
    parser.add_argument("-k", '--key', type=str, default='decipher_key.py', help='decipher key')
    args = parser.parse_args()
    
    print(f"The name of input file is: {args.input_file_name}")
    print(f"The name of periodicity file is: {args.periodicity_file_name}")
    print(f"The name of output file is: {args.output_file_name}")
    print(f"The name of file with key is: {args.key}")

    try:
        text = read_file(args.input_file_name)
        periodicity = get_periodicity(text)
        write_file(periodicity, args.periodicity_file_name)
        result_text = periodicity_analysis(text, key)
        write_file(result_text, args.output_file_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__" :
    main()