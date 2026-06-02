import hashlib
import os
from tqdm import tqdm


def read_file(text_file):
  """
  читает содержимое файла в байтах
  
  arguments: 
        text_file: путь к файлу, из которого будет считываться содержимое, строка
  return:
        bytes_content: содержимое файла в байтах
  """
  try:
    with open(text_file, 'rb') as file: 
      bytes_content = file.read()

    return bytes_content
  except FileNotFoundError:
    raise FileNotFoundError(f"{text_file} file was not found")
  except Exception as error:
    print(f"Error has occurred: {error}")


def calculate_hash(text_file):
  """
  вычисляет хеш для содержимого выбранного файла

  arguments:
        text_file: путь к файлу, хеш содержимого которого надо вычислить, строка
  return:
        result_hash: вычисленный хеш содержимого файла, строка
  """

  hasher = hashlib.sha256()
  bytes_content = read_file(text_file)
  hasher.update(bytes_content)
  result_hash = hasher.hexdigest()

  return result_hash


def write_hash(file_name, result_hash):
  """
  записывает полученный хеш в файл

  arguments:
        file_name: путь к файлу для записи хеша, строка
        result_hash: вычисленный хеш, строка
  return: -
  """

  with open(file_name, 'w', encoding="utf-8") as file:
    file.write(result_hash)


def read_hash(file_with_hash):
  """
  читает хеш из файла

  arguments:
        file_with_hash: путь к файлу, из которого надо прочитать хеш, строка
  return:
        hash_from_file: прочитанный из файла хеш, строка
  """
  try:
    with open(file_with_hash, 'r', encoding="utf-8") as file: 
      hash_from_file = file.read()

    return hash_from_file
  except FileNotFoundError:
    raise FileNotFoundError(f"{file_with_hash} file was not found")
  except Exception as error:
    print(f"Error has occurred: {error}")


def hash_comparison(text_file, file_with_hash):
  """
  проверяет целостность файла, сравнивая хеш, ранее записанный в файл, и хеш, вычисленный только что для данного файла

  arguments:
        text_file: путь к файлу, хеш которого надо вычислить, строка
        file_with_hash: путь к файлу, из которого надо прочитать хеш, строка
  return:
        result: словарь:
                  comparison: True, если хеши совпали, иначе False, логический тип
                  calculated_hash: хеш, вычисленный для данного файла, строка
                  hash_from_file: хеш, ранее записанный в файл, строка
  """

  calculated_hash = calculate_hash(text_file)
  hash_from_file = read_hash(file_with_hash)

  result = {}

  comparison = calculated_hash == hash_from_file
  result["comparison"] = comparison
  result["calculated hash"] = calculated_hash
  result["hash from file"] = hash_from_file

  return result


def clear_hash_file(file_with_hash):
  """
  удаляет файл, в котором сохранен хеш, если он существует

  arguments:
        file_with_hash: путь к файлу, в котором сохранен хеш, строка
  return: -
  """

  try:
    if os.path.exists(file_with_hash):
      os.remove(file_with_hash)
  except FileNotFoundError:
    raise FileNotFoundError(f"{file_with_hash} file was not found")
  except Exception as error:
    print(f"Error has occurred: {error}")


def find_part_collision(text_file, part_len = 4, max_iters = 1000000):
  """
  ищет частичную коллизию с хешем, вычисленным для файла

  arguments:
        part_len: количество символов, которые должны совпасть у хешей (по умолчанию 4), целое число
  return:
        result: словарь:
                  collision: True, если найдена коллизия, иначе False, логический тип
                  number of steps: количество шагов, за которые найдена или не найдена коллизия, целое число

                  в случае collision: True - сведения о том, с какой строкой найдена коллизия
  """
  try:
    if part_len < 1 or part_len > 5:
      raise ValueError("must be a number from 1 to 5")

    result = {}

    calculated_hash = calculate_hash(text_file)
    part = calculated_hash[:part_len]

    for i in tqdm(range(max_iters), desc = f"Search for matches with {part}", unit = "hash"):
      new_string = f"i_love_corgis_{i}"
      new_hash = hashlib.sha256(new_string.encode("utf-8")).hexdigest()

      if new_hash.startswith(part):
        result["collision"] = True
        result["number of steps"] = i
        result["text file"] = text_file
        result["calculated hash"] = calculated_hash
        result["string"] = new_string
        result["hash from string"] = new_hash

        return result

    result["collision"] = False
    result["number of steps"] = max_iters

    return result

  except Exception as error:
    print(f"Error has occurred: {error}")

    result = {}
    result["collision"] = False
    result["error"] = str(error)
    result["number of steps"] = 0
    
    return result