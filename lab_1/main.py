import task1_polybius
import task2_frequency

def main():
    print("="*80)
    print("ЛАБОРАТОРНАЯ РАБОТА №1")
    print("Простейшие методы шифрования")
    print("="*80)
    
    while True:
        print("\n1. Задание 1 (Квадрат Полибия)")
        print("2. Задание 2 (Частотный анализ, вар.11)")
        print("3. Оба задания")
        print("0. Выход")
        
        choice = input("Выбор: ").strip()
        
        if choice == '1':
            task1_polybius.run()
        elif choice == '2':
            task2_frequency.run()
        elif choice == '3':
            task1_polybius.run()
            task2_frequency.run()
        elif choice == '0':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()