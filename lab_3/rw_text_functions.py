def read_text_file(initial_text_file: str) -> bytes:
    """
    reads initial text from file and converts it to bytes for encryption
    
    arguments: 
            initial_text_file: path to initial text file, in str
    return:
            text: initial text in bytes
    """
    try:
        with open(initial_text_file, "r", encoding="utf-8") as file:
            text = file.read()
        return text.encode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"{initial_text_file} file was not found")


def write_encrypt_text(file_name: str, iv: bytes, c_text: bytes) -> None:
    """
    saves encrypted text and initialization vector to file
    
    arguments: 
            file_name: path to file to save encrypted text, in str
            iv: initialization vector (16 random bytes)
            c_text: encrypted text in bytes
    return: -
    """
    try:
        with open(file_name, "wb") as file:
            file.write(iv + c_text)
    except Exception as e:
        raise Exception(f"Failed to write encrypted text to {file_name}: {e}")


def read_encrypt_text(encrypted_text_file: str) -> tuple:
    """
    reads encrypted text from file and separates text and initialization vector for decryption
    
    arguments: 
            encrypted_text_file: path to file with encrypted text, in str
    return:
            tuple(iv, c_text): tuple with initialization vector (16 bytes) and encrypted text in bytes 
    """
    try:
        with open(encrypted_text_file, 'rb') as file:
            content = file.read()
        
        iv = content[:16]
        c_text = content[16:]
        
        return iv, c_text
    except FileNotFoundError:
        raise FileNotFoundError(f"{encrypted_text_file} file was not found")


def write_decrypt_text(file_name: str, unpadded_dc_text: bytes) -> None:
    """
    saves decrypted text to file
    
    arguments: 
            file_name: path to file to save decrypted text, in str
            unpadded_dc_text: decrypted text without padding in bytes
    return: -
    """
    try:
        with open(file_name, 'wb') as file:
            file.write(unpadded_dc_text)
    except Exception as e:
        raise Exception(f"Failed to write decrypted text to {file_name}: {e}")