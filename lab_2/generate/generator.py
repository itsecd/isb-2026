# -*- coding: utf-8 -*-

import random


def main():
    """Main generator function"""
    sequence: str = ""
    
    for _ in range(128):
        bit: int = random.randint(0,1)
        sequence += str(bit)

    print(sequence)


if __name__ == "__main__":
    main()
