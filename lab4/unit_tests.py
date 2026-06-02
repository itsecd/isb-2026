import unittest
import os
from work_with_hash import calculate_hash, write_hash, read_hash, hash_comparison, clear_hash_file, find_part_collision


class TestHashFunctions(unittest.TestCase):
  
  def setUp(self):
    """
    подготавливает файлы для теста
    """

    self.test_file = "test_file.txt"
    self.hash_file = "hash_file.txt"

    with open(self.test_file, "w", encoding="utf-8") as file:
      file.write("According to Welsh legend, corgis became a gift to people from noble fairies.")

    calculated_hash = calculate_hash(self.test_file)
    write_hash(self.hash_file, calculated_hash)


  def tearDown(self):
    """
    удаляет файлы после теста
    """

    if os.path.exists(self.test_file):
      os.remove(self.test_file)
    if os.path.exists(self.hash_file):
      os.remove(self.hash_file)


  def test_write_and_read(self):
    """
    проверяет корректность записи хеша в файл и его чтения
    """

    sample_hash = "1234567890abcdef" * 4
    write_hash(self.hash_file, sample_hash)

    hash_from_file = read_hash(self.hash_file)

    self.assertEqual(hash_from_file, sample_hash)


  def test_hash_length(self):
    """
    проверяет, что длина хеша 64 символа
    """

    hash_from_file = read_hash(self.hash_file)
    self.assertEqual(len(hash_from_file), 64)


  def test_integrity_when_not_changed(self):
    """
    проверяет целостность: хеши должны совпасть, если в файл не вносили изменения
    """

    current_hash = calculate_hash(self.test_file)
    write_hash(self.hash_file, current_hash)

    result = hash_comparison(self.test_file, self.hash_file)
    self.assertTrue(result["comparison"])


  def test_integrity_when_changed(self):
    """
    проверяет целостность: хеши не должны совпасть, если в файл вносили изменения
    """

    current_hash = calculate_hash(self.test_file)
    write_hash(self.hash_file, current_hash)

    with open(self.test_file, "a", encoding="utf-8") as file:
      file.write("Corgis are very cute.")

    result = hash_comparison(self.test_file, self.hash_file)
    self.assertFalse(result["comparison"])


  def test_clear_file(self):
    """
    проверяет удаление файла хешем
    """

    write_hash(self.hash_file, "hash123")
    self.assertTrue(os.path.exists(self.hash_file))

    clear_hash_file(self.hash_file)
    self.assertFalse(os.path.exists(self.hash_file))


  def test_collision_wrong_length(self):
    """
    проверяет, что функция коллизий возвращает ошибку при неверном количестве совпадающих символов
    """

    result_low = find_part_collision(self.test_file, part_len=0)
    self.assertIn("error", result_low)

    result_high = find_part_collision(self.test_file, part_len=6)
    self.assertIn("error", result_high)


if __name__ == "__main__":
  unittest.main()