import os
import json
from typing import Dict, Any


REQUIRED_SETTINGS: List[str] = [
    "sym_key_length", "initial_file", "encrypted_file", "decrypted_file", 
    "symmetric_key", "public_key", "private_key"
]

FOLDERS: Dict[str, str] = {
    "text": "./texts",
    "key":  "./keys"
}


def read_json_file(filename: str) -> Dict[str, Any]:
    '''
    Reading input parameters from .json file.

    Args:
        filename (str): The name of the file with input parameters.

    Returns:
        Dict[str, Any]: Dictionary with input parameters.

    Raises:
        FileNotFoundError: If file is not found.
    '''

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} is not found")

    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def settings_validation_check(settings: Dict[str, Any]) -> None:
    '''
    Checks for all input parameters.

    Args:
        settings (Dict[str, Any]): The dictionary that is being checked.

    Returns:
        None: All input parameters exist.

    Raises:
        KeyError: One or more input parameters are missing.
    '''

    missing_parameters = [parameter for parameter in REQUIRED_SETTINGS if parameter not in settings]

    if missing_parameters:
        raise KeyError(f"In settings.json missed input parameters: {", ".join(missing_parameters)}")

    return None


def write_file_bytes(filename: str, data: bytes, mode: str) -> None:
    '''
    Serializing the data in bytes to a file,
    automatically creating directory if it does not exist.

    Args:
        filename (str): The name of the file where to write the data.
        data (bytes): A data in bytes.
        mode (str): A type of data.

    Returns:
        None: The message is displayed that the data is written to the file.
    
    Raises:
        ValueError: If the file name does not contain the extension
                    or invalid mode.
    '''

    if mode not in FOLDERS:
        raise ValueError(f"Invalid mode '{mode}'. Expected 'text' or 'key'")

    folder = FOLDERS[mode]

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    pure_filename = os.path.basename(filename)
    name, ext = os.path.splitext(pure_filename)
    if not ext:
        raise ValueError(f"{pure_filename} is an invalid file name. Please add the extension .txt")

    right_filename = os.path.join(folder, pure_filename)
    with open(right_filename, 'wb') as file:
        file.write(data)
    
    print(f"The data is written on the path {right_filename}")
    

def read_file_bytes(filename: str, mode: str) -> bytes:
    '''
    Deserialization of the data in bytes.

    Args:
        filename (str): The name of the file where to read the data.
        mode (str): A type of data.

    Returns:
        bytes: The data in bytes.
    
    Raises:
        ValueError: If the file name does not contain the extension
                    or invalid mode.
        FileNotFoundError: If file is not found.
    '''

    if mode not in FOLDERS:
        raise ValueError(f"Invalid mode '{mode}'. Expected 'text' or 'key'")

    folder = FOLDERS[mode]

    pure_filename = os.path.basename(filename)
    name, ext = os.path.splitext(pure_filename)
    if not ext:
        raise ValueError(f"{pure_filename} is an invalid file name. Please add the extension .txt")

    right_filename = os.path.join(folder, pure_filename)
    if not os.path.exists(right_filename):
        raise FileNotFoundError(f"File {right_filename} is not found")

    with open(right_filename, 'rb') as file:
        return file.read()
    

def read_initial_text(filename: str) -> str:
    '''
    Reads the initial text from a file and decodes it to a string.

    Args:
        filename (str): The name of the file where to read the data.

    Returns:
        str: The initial text of the file as a regular string.

    Raises:
        ValueError: If the file name does not contain the extension
                    or invalid mode.
        FileNotFoundError: If the file is not found.
    '''

    text_bytes = read_file_bytes(filename, mode='text')
    text = text_bytes.decode('utf-8')

    return text


def write_decrypted_text(filename: str, text: str) -> None:
    '''
    Encodes decrypted text string to bytes and saves it to a file.

    Args:
        filename (str): The name of the file where to write the data.
        text (str): The decrypted text string to save.

    Returns:
        None: The message is displayed that the data is written to the file.
    '''

    text_bytes = text.encode('utf-8')
    write_file_bytes(filename, text_bytes, mode="text")
