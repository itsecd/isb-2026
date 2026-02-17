def save(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def read(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
    
GRILLE = [
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
]

def rotate(g):
    n = len(g)
    return [[g[n-1-j][i] for j in range(n)] for i in range(n)]

def encrypt(text):
    text = text.upper().replace(' ', '_')
    n = len(GRILLE)
    block_size = n * n * 4  #64 символа на блок
    
    blocks = []
    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        blocks.append(block)
    
    result = ''
    
    for block in blocks:
        if len(block) < block_size:
            block += 'Ъ' * (block_size - len(block))
    
        m = [[''] * n for _ in range(n)]
    
        pos = 0
        g = GRILLE
        for _ in range(4):
            for i in range(n):
                for j in range(n):
                    if g[i][j]:
                        m[i][j] = block[pos]
                        pos += 1
            g = rotate(g)
        
        for i in range(n):
            for j in range(n):
                result += m[i][j]
    
    return result

input_file = 'input.txt'  #файл с исходным текстом
text = read(input_file)

enc = encrypt(text)

save('encrypted.txt', enc)  

with open('key.txt', 'w', encoding='utf-8') as f:
    f.write('Решетка Кардано 4x4:\n')
    for row in GRILLE:
        f.write(''.join(['0' if x else '1' for x in row]) + '\n')
    f.write(f'\nРазмер блока: {len(GRILLE)*len(GRILLE)*4} символов\n')
    f.write(f'Всего блоков: {(len(text) + 63) // 64}\n')

print(f'Размер текста: {len(text)} символов')
print(f'Размер блока: {len(GRILLE)*len(GRILLE)*4} символов')
print(f'Количество блоков: {(len(text) + 63) // 64}')


