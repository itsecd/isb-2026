RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_LENGTH = len(RUSSIAN_ALPHABET)

TASK1_ORIGINAL_FILE = "task1/source.txt"
TASK1_ENCRYPTED_FILE = "task1/encrypted.txt"
TASK1_KEY_FILE = "task1/key.txt"

TASK2_ORIGINAL_FILE = "task2/cod19.txt"
TASK2_FREQUENCIES_FILE = "task2/frequencies.txt"
TASK2_DECRYPTED_FILE = "task2/decrypted.txt"
TASK2_KEY_FILE = "task2/key.txt"

RUSSIAN_FREQUENCIES = [
    (' ', 0.128675),
    ('О', 0.096456),
    ('И', 0.075312),
    ('Е', 0.072292),
    ('А', 0.064841),
    ('Н', 0.061820),
    ('Т', 0.061619),
    ('С', 0.051953),
    ('Р', 0.040677),
    ('В', 0.039267),
    ('М', 0.029803),
    ('Л', 0.029400),
    ('Д', 0.026983),
    ('П', 0.026379),
    ('К', 0.025977),
    ('У', 0.024768),
    ('З', 0.015908),
    ('Ы', 0.015707),
    ('Ь', 0.015103),
    ('Б', 0.013290),
    ('Ч', 0.011679),
    ('Ж', 0.010673),
    ('Г', 0.009867),
    ('Х', 0.008659),
    ('Ф', 0.007249),
    ('Й', 0.006847),
    ('Ю', 0.006847),
    ('Я', 0.006645),
    ('Ц', 0.005034),
    ('Ш', 0.004229),
    ('Щ', 0.003625),
    ('Э', 0.002416),
    ('Ъ', 0.000000)
]

RUSSIAN_FREQUENCIES_SORTED = sorted(RUSSIAN_FREQUENCIES, key=lambda x: x[1], reverse=True)