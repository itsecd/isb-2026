import random
import secrets 

class BinarySequenceGenerator:
    """Класс для генерации бинарных последовательностей"""
    
    def __init__(self, length: int = 128, use_secrets: bool = False):
        self.length = length
        self.sequence = ""
        self.generator = secrets if use_secrets else random
        
    def generate(self) -> str:
        """Генерирует последовательность"""
        bits = []
        for _ in range(self.length):
            bits.append(str(self.generator.randrange(2)))
        self.sequence = ''.join(bits)
        return self.sequence
    
    def save(self, filename: str = "output.txt") -> bool:
        """Сохраняет последовательность в файл"""
        try:
            with open(filename, 'w') as file_handle:
                file_handle.write(self.sequence)
            return True
        except IOError:
            return False

def main():
    # Создаем экземпляр генератора
    generator = BinarySequenceGenerator(length=128)
    
    # Генерируем последовательность
    result = generator.generate()
    
     # Сохраняем результат
    success = generator.save("python_sequence.txt")
    
if __name__ == "__main__":
    main()