# constants.py
ALPHABET: str = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
KEY_CHARSET: str = ''.join(chr(i) for i in range(0x2500, 0x2580))
REFERENCE_ORDER: list[str] = [
    ' ', 'О', 'И', 'Е', 'А', 'Н', 'Т', 'С', 'Р', 'В', 'М', 'Л', 'Д', 'Я', 'К', 'П',
    'З', 'Ы', 'Ь', 'У', 'Ч', 'Ж', 'Г', 'Х', 'Ф', 'Й', 'Ю', 'Б', 'Ц', 'Ш', 'Щ', 'Э', 'Ъ'
]
ENCRYPTED_FILE = 'encrypted.txt'
KEY_FILE = 'key.txt'
DECRYPTED_CHECK_FILE = 'decrypted_check.txt'
DECRYPTED_TEXT = 'decrypted.txt'