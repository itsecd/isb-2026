def intput_file(filename: str) -> str:
    try:
        file = open(filename, "r", encoding="utf-8")
        print(f"File {filename} ready to work")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print("Sorry, this file impossible to detect")
        return ""
    
def output_file(filename: str, text: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
        file.write("\n")    

start_string = intput_file("text.txt")

polybius_square = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I/J', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]

key_str = intput_file("key.txt").strip()
shift = int(key_str) if key_str else 1

produce_string = ""
for liter in start_string:
    if liter.isalpha():
        produce_string += liter.upper()

number_vector = []
for liter in produce_string:
    found = False
    for i in range(5):
        for j in range(5):
            cell = polybius_square[i][j]
            if cell == 'I/J':
                if liter in ('I', 'J'):
                    number_vector.append([i, j])
                    found = True
                    break
            elif liter == cell:
                number_vector.append([i, j])
                found = True
                break
        if found:
            break

final_string = ""
for pair in number_vector:
    i, j = pair[0], pair[1]
    new_i = (i + shift) % 5
    buffer = polybius_square[new_i][j]
    if buffer == 'I/J':
        buffer = 'I'
    final_string += buffer

output_file("code.txt", final_string)