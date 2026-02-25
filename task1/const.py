ALPHABET = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5,
    'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9, 'И': 10,
    'Й': 11, 'К': 12, 'Л': 13, 'М': 14, 'Н': 15,
    'О': 16, 'П': 17, 'Р': 18, 'С': 19, 'Т': 20,
    'У': 21, 'Ф': 22, 'Х': 23, 'Ц': 24, 'Ч': 25,
    'Ш': 26, 'Щ': 27, 'Ъ': 28, 'Ы': 29, 'Ь': 30,
    'Э': 31, 'Ю': 32, 'Я': 33, '.': 34, ',': 35, '-': 36, ' ': 37
}

ALPHABET_BY_NUMBER = {i: k for k, i in ALPHABET.items()}

TEXT_ORIGINAL='text1_original.txt'

TASK1_ENCRYPTION='task1_encryption.txt'

TASK1_DECRYPTION='task1_decryption.txt'

KEY='key.txt'