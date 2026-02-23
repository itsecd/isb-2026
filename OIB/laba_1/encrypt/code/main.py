import argparse 
from caesar import caesar_encrypt, caesar_decrypt
from rw import read, write 

def parser_args():
    parser = argparse.ArgumentParser(description="Шифр Цезаря.")
    
    parser.add_argument("-m", "--mode", 
                        type=str, 
                        required=True, 
                        choices=['encrypt', 'decrypt'],
                        help="Режим работы: 'encrypt' (шифрование) или 'decrypt' (дешифрование).")
    
    parser.add_argument("-po", "--path_original", type=str, required=True, help="Путь к исходному файлу (для чтения).")
    parser.add_argument("-pe", "--path_result", type=str, required=True, help="Путь к файлу для сохранения результата.")
    parser.add_argument("-n", "--number", type=int, required=True, help="Число для сдвига.")

    args = parser.parse_args()
    return args.mode, args.path_original, args.path_result, args.number 

if __name__ == "__main__":
    mode, path_original, path_result, number = parser_args()

    text_to_process = read(path_original)
    
    if not text_to_process:
        print("Не удалось прочитать исходный файл. Завершение работы.")
    else:
        processed_text = ""
        
        if mode == 'encrypt':
            print(f"Выбран режим: ШИФРОВАНИЕ (сдвиг {number})")
            processed_text = caesar_encrypt(text_to_process, number)
            
        elif mode == 'decrypt':
            print(f"Выбран режим: ДЕШИФРОВАНИЕ (сдвиг {number})")
            processed_text = caesar_decrypt(text_to_process, number)
            

        if processed_text:
            write(path_result, processed_text)
