ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789.,!?«»"

def find_pos(matrix: list, a: str) -> str:
    for i in range(7):
        for j in range(7):
            if matrix[i][j] == a:
                return str(i+1)+str(j+1)
    return None

def alphabet_to_matrix() -> list:
    with open ("key.txt", encoding='utf-8') as f:
        key = f.read().strip()
    matrix = [[0 for _ in range(7)] for _ in range(7)]
    val = 0
    key = key.upper()
    alphabet = ''
    for i in key:
        if i not in alphabet:
            alphabet += i
        else:
            continue
    for i in ALPHABET:
        if i not in alphabet:
            alphabet += i
        else: 
            continue
    if (len(alphabet) != 49):
        print("текст в ключе содержит неизвестные символы, проверьте ключ")
        return None
    for i in range(7):
        for j in range(7):
            matrix[i][j] = alphabet[val]
            val += 1
    return matrix

def translate_to_positions(path: str, matrix: str) -> str:
    if matrix == None:
        return None
    with open(path, encoding='utf-8') as f:
        t = f.read()
    text = t.upper()
    string = ''
    for i in range (len(text)):
            string += find_pos(matrix, text[i]) + ' ' if find_pos(matrix, text[i]) != None else text[i]
    return string

def uncoding(string: str) -> str:
    matrix = alphabet_to_matrix()
    if matrix == None:
        return None
    text = ''
    cipher = string.split(' ')
    for i in cipher:
        if i == '':
            text +=' '
        elif i.isdigit() and len(i) == 2:
            text += matrix[int(i[0])-1][int(i[1])-1]
        else:
            text += i
    return text


def main() -> None:
    encrypted = translate_to_positions("input.txt", alphabet_to_matrix())
    with open ("output.txt", 'w', encoding='utf-8') as file:
        file.write(encrypted)
    print(encrypted)
    print('\n')
    print (uncoding(encrypted))
if __name__ == "__main__":
    main()