import random

def generate_and_write_sequence(n: int, seed: int, output_path: str) -> None:
    random.seed(seed)
    
    sequence_bits = []

    for _ in range(n):
        bit = random.getrandbits(1)
        sequence_bits.append(str(bit))

    try:
        with open(output_path, 'w') as f:
            f.write("".join(sequence_bits))
    except IOError as e:
        print(f"Ошибка при записи файла: {e}")

if __name__ == "__main__":
    N = 128
    SEED = 11342 
    OUTPUT_FILE = "seq_py.txt"

    generate_and_write_sequence(N, SEED, OUTPUT_FILE)