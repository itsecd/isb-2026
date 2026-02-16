polybius_square = [
    ['А', 'Б', 'В', 'Г', 'Д', 'Е'],
    ['Ё', 'Ж', 'З', 'И', 'Й', 'К'],
    ['Л', 'М', 'Н', 'О', 'П', 'Р'],
    ['С', 'Т', 'У', 'Ф', 'Х', 'Ц'],
    ['Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь'],
    ['Э', 'Ю', 'Я', ',', '-', '.']  
]
def encryption(text):
    text = text.upper()
    result = []
    
    for char in text:
        if char == ' ':
            result.append('68')
            continue
            
        for row in range(6):
            for col in range(6):
                if polybius_square[row][col] == char:
                    result.append(str(row + 1) + str(col + 1))
                    break
    
    return ' '.join(result)

