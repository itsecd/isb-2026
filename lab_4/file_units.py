import os
import json
from typing import Dict, Any, Optional


DB_SALT = "users_salted.json"
DB_NOSALT = "users_nosalt.json"


def read_json_file(filename: str) -> Dict[str, Any]:
    """
    Reads a JSON file into a Python dictionary.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The parsed data from the file.
    """

    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def write_json_file(filename: str, data: Dict[str, Any]) -> None:
    """
    Saves a Python dictionary to a JSON file.

    Args:
        filename (str): The path to the destination JSON file.
        data (Dict[str, Any]): The dictionary data to save.
    """

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def safe_load_database(filename: str) -> Optional[Dict[str, Any]]:
    """
    Saves the database, considering all exceptions.

    Args:
        filename (str): Path to a .json file

    Returns:
        Optinal[Dict[str, Any]]: The database dictionary, or None if corrupted.
    """

    try:
        database = read_json_file(filename)
        return database

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print(f"Error: Something went wrong with the file!\n"
              f"Inform minialbina about the code tampering.")
        return None