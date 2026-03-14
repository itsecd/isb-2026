import random
import sys
import config

def generate_sequence(seed=config.SEED, n=config.N, filename=None):
    random.seed(seed)
    bits = [str(random.getrandbits(1)) for _ in range(n)]
    seq = ''.join(bits)

    if filename:
        with open(filename, 'w') as f:
            f.write(seq + '\n')
    else:
        print(seq)

if __name__ == '__main__':
    
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    generate_sequence(filename=filename)