import secrets
from settings import BIT, FILENAME

def secure_bits(length: int) -> str:
    """Генерирует криптостойкую двоичную строку заданной длины."""
    byte_count = (length + 7) // 8
    rand_bytes = secrets.token_bytes(byte_count)
    bits = ''.join(f'{b:08b}' for b in rand_bytes)[:length]
    return bits

def save_to_file(filename: str, content: str) -> None:
    with open(filename, 'w') as f:
        f.write(content)

def main():
    bits_str = secure_bits(BIT)
    save_to_file(FILENAME, bits_str)
    print(f"Сгенерировано {BIT} бит в файл {FILENAME}")

if __name__ == "__main__":
    main()