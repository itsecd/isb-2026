def read_text_file(initial_file):
        """
        считывание исходного текста из файла и преобразование его в байты для шифрования

        аргументы: путь к исходному текстовому файл

        возвращает: начальный текст в байтах

        """
        try:
                with open(initial_file, "r", encoding="utf-8") as file:
                        text = file.read()
                return text.encode('utf-8')

        except FileNotFoundError:
                raise FileNotFoundError(f"Нет такого файла {initial_file}")
        


def write_encrypt_text(encrypted_file, iv, etext_in_bytes):
        """
        сохранение зашифрованного текста и вектора инициализации в файл
        аргументы: 
                encrypted_file: путь к файлу для сохранения зашифрованного текста
                iv: вектор инициализации (16 случайных байтов)
                etext_in_bytes: зашифрованный текст в байтах
        возвращает: ничегошеньки
        """
        try:
                with open(encrypted_file, "wb") as file:
                        file.write(iv + etext_in_bytes)

        except FileNotFoundError:
                raise FileNotFoundError(f"Нет такого файла {encrypted_file}")
        


def read_encrypt_text(encrypted_file):
        """
        считывание зашифрованного текста из файла и разделение текста и вектора инициализации для расшифровки
        аргументы: 
                encrypted_file: путь к файлу с зашифрованным текстом
                
        возвращает:
                tuple(iv, etext_in_bytes): кортеж с вектором инициализации (16 случайных байтов) и зашифрованным текстом в байтах  
        """

        try:
                with open(encrypted_file, 'rb') as file: 
                        content = file.read()

                iv = content[:16]
                etext_in_bytes = content[16:]

                return iv, etext_in_bytes

        except FileNotFoundError:
                raise FileNotFoundError(f"Такой файл мы не находили {encrypted_file}")


def write_decrypt_text(decrypted_file_in_bytes, decrypted_file):
        """
        сохранение расшифрованного текста в файл
        аргументы: 
                decrypted_file_in_bytes: путь к файлу для сохранения расшифрованного текста, в виде строки
                decrypted_file: расшифрованный текст без заполнения в байтах
        возвращает: совсем ничего
        """
        try:
                with open(decrypted_file_in_bytes, 'wb') as file: 
                        file.write(decrypted_file)
                        
        except FileNotFoundError:
                raise FileNotFoundError(f"Такой файл мы не находили {decrypted_file_in_bytes}")
