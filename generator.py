import secrets
import os

def generate_secure(filename, num_bits=128):
    os.makedirs("sequences", exist_ok=True)
    with open(filename, 'w') as f:
        for _ in range(num_bits):
            f.write(str(secrets.randbits(1)))

if __name__ == "__main__":
    generate_secure("sequences/sequence_python.txt")
    print("Готово! 128 бит сохранено в sequences/sequence_python.txt")
