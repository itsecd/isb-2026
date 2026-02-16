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

def recording_key(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Квадрат Полибия (ключ шифрования):\n")
        f.write("   1 2 3 4 5 6\n")
        for i, row in enumerate(polybius_square, 1):
            f.write(f"{i}  {' '.join(row)}\n")

text = """В современном мире информация стала ценнейшим ресурсом, а её защита —
вопросом выживания для бизнеса и спокойствия для частных лиц. Информационная безопасность — это не просто
установка антивируса, а комплексный подход, 
включающий защиту данных от кражи, повреждения или несанкционированного доступа.
Угрозы подстерегают нас повсюду от фишинговых писем и вредоносного ПО до небезопасного
интернета в кафе. Слабый пароль или невнимательность могут привести к утечке паспортных данных,
банковских реквизитов или коммерческой тайны. Основные правила цифровой гигиены просты: используйте 
сложные уникальные пароли и двухфакторную аутентификацию, регулярно обновляйте программы, не переходите
по подозрительным ссылкам. Помните, ваша безопасность в цифровом мире на девяноста процентов зависит от вашей же осмотрительности."""

encrypted_text = encryption(text)

with open('Task1_original_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

with open('Task1_encrypted_text.txt', 'w', encoding='utf-8') as f:
    f.write(encrypted_text)

recording_key('Task1_encryption_key.txt')

print(f"\nШифрование успешно завершено")