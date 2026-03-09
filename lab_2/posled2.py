import random
import sys

def main():
    
    try:
        bits = ''.join(str(random.randint(0, 1)) for _ in range(128))
        
        try:
            with open("python_posled.txt", "w") as f:
                f.write(bits + "\n")
        except IOError as e:
            print(f"Error when writing to a file: {e}")
            sys.exit(1)
        
        print("Python sequence (128 bit):")
        formatted = ' '.join(bits[i:i+8] for i in range(0, 128, 8))
        print(formatted)
        print("save in python_posled.txt")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()