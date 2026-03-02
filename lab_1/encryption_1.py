alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
square_size = 6


def build_square_table(alphabet, square_size):
    square_table = []

    for i in range(0, len(alphabet), square_size):
        square_table.append(alphabet[i:i + square_size])

    return square_table


def encrypt(text, square_table):
    result = ""

    for letter in text:
        for row in range(len(square_table)):
            if letter in square_table[row]:
                column = square_table[row].index(letter)
                result += str(row + 1) + str(column + 1) + " "

    return result


def decrypt(cipher_text, square_table):
    result = ""

    numbers = cipher_text.split()

    for pair in numbers:
        row = int(pair[0]) - 1
        column = int(pair[1]) - 1
        result += square_table[row][column]

    return result


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def save_key(square, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for row in square:
            file.write(row + "\n")


def clean_text(text, alphabet):
    result = ""

    for char in text.upper():
        if char in alphabet:
            result += char

    return result


def main():
    square = build_square_table(alphabet, square_size)

    text = read_file("text_1.txt")
    text = clean_text(text, alphabet)

    write_file("check_cleanText.txt", text)

    cipher = encrypt(text, square)
    write_file("result_1.txt", cipher)

    decrypted = decrypt(cipher, square)
    write_file("Result_decText1.txt", decrypted)

    save_key(square, "key_text1.txt")

    print("Зашифрование и дешифрование текста выполнено.")


if __name__ == "__main__":
    main()