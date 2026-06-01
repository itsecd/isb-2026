import unittest
import utils
import hash
import collisions

class TestHashCollisionApp(unittest.TestCase):

    def test_random_string_generation_valid(self):
        """
        Проверка генерации строки правильной длины
        """
        s = utils.generate_random_string(10)
        self.assertEqual(len(s), 10)
        self.assertIsInstance(s, str)

    def test_random_string_generation_invalid(self):
        """
        Проверка реакции на некорректную длину строки
        """
        with self.assertRaises(ValueError):
            utils.generate_random_string(-5)
        with self.assertRaises(ValueError):
            utils.generate_random_string("not_an_int")

    def test_sha256_hashing(self):
        """
        Проверка возврата байтового представления хэша
        """
        h_bytes = hash.find_hash_sha256("test_string")
        self.assertIsInstance(h_bytes, bytes)
        self.assertEqual(len(h_bytes), 32)

    def test_shortened_hash_bounds(self):
        """
        Проверка на попадание укороченного хэша в диапазон бит
        """
        h_bytes = hash.find_hash_sha256("hello")
        
        for bits in [8, 12, 16]:
            short_h = hash.find_shortened_hash(h_bytes, bits)
            self.assertIsInstance(short_h, int)
            self.assertGreaterEqual(short_h, 0)
            self.assertLess(short_h, 2 ** bits)

    def test_find_collision_logic(self):
        """
        Проверка на то, что функция поиска действительно находит коллизию
        """
        res = collisions.find_collision(hash_len=8, str_len=10, disable_tqdm=True)
        self.assertIsNotNone(res)
        s1, s2, h, attempts = res
        self.assertNotEqual(s1, s2)
        
        h1 = hash.find_shortened_hash(hash.find_hash_sha256(s1), 8)
        h2 = hash.find_shortened_hash(hash.find_hash_sha256(s2), 8)
        self.assertEqual(h1, h2)
        self.assertEqual(h1, h)

if __name__ == "__main__":
    unittest.main()