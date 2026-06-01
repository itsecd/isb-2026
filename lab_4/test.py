import unittest
import create
import packet
import atak
import collision


class TestHMACSystem(unittest.TestCase):
    def setUp(self):
        """
        Инициализирует базовые тестовые данные перед каждым тестом.

        """
        self.key = "test_secret_key"
        self.text = "Тестовое сообщение"
        self.expected_hmac = create.create(self.text, self.key)

    def test_create_success(self):
        """
        Проверяет успешное формирование корректного HMAC-SHA256 хэша.

        """
        result = create.create(self.text, self.key)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_create_invalid_types(self):
        """
        Проверяет генерацию TypeError при передаче нестроковых типов данных.

        """
        with self.assertRaises(TypeError):
            create.create(123, self.key)
        with self.assertRaises(TypeError):
            create.create(self.text, None)

    def test_create_empty_values(self):
        """
        Проверяет генерацию ValueError при передаче пустых строк.

        """
        with self.assertRaises(ValueError):
            create.create("", self.key)
        with self.assertRaises(ValueError):
            create.create(self.text, "")

    def test_verify_success(self):
        """
        Проверяет успешную верификацию данных с правильной подписью.

        """
        self.assertTrue(create.verify(self.text, self.key, self.expected_hmac))

    def test_verify_fail(self):
        """
        Проверяет отклонение проверки при измененном тексте или неверной подписи.

        """
        self.assertFalse(create.verify("Измененный текст", self.key, self.expected_hmac))
        self.assertFalse(create.verify(self.text, self.key, "wrong_hmac_hex"))

    def test_transmit_packet_structure(self):
        """
        Проверяет корректность структуры и типов полей сформированного сетевого пакета.

        """
        pkt = packet.transmit_packet(self.text, self.expected_hmac)
        self.assertIsInstance(pkt, dict)
        self.assertIn("data", pkt)
        self.assertIn("hmac_hex", pkt)
        self.assertEqual(pkt["data"], self.text)
        self.assertEqual(pkt["hmac_hex"], self.expected_hmac)

    def test_verify_packet_valid(self):
        """
        Проверяет успешное прохождение валидации для оригинального пакета.

        """
        pkt = {"data": self.text, "hmac_hex": self.expected_hmac}
        self.assertTrue(packet.verify_packet(pkt, self.key))

    def test_verify_packet_invalid_structure(self):
        """
        Проверяет реакцию валидатора на пакет с нарушенной структурой полей.

        """
        broken_pkt = {"wrong_field": self.text, "hmac_hex": self.expected_hmac}
        with self.assertRaises(KeyError):
            packet.verify_packet(broken_pkt, self.key)

    def test_simulate_attack(self):
        """
        Проверяет, что при атаке текст меняется, а старая подпись сохраняется в пакете.

        """
        orig_pkt = {"data": self.text, "hmac_hex": self.expected_hmac}
        new_text = "Вредоносный текст"
        spoiled_pkt = atak.simulate_atak(orig_pkt, new_text)
        
        self.assertEqual(spoiled_pkt["data"], new_text)
        self.assertEqual(spoiled_pkt["hmac_hex"], orig_pkt["hmac_hex"])
        self.assertFalse(packet.verify_packet(spoiled_pkt, self.key))

    def test_find_collision(self):
        msg1, msg2, shared_hmac = collision.find_collision(self.key, difficulty=2)
        self.assertNotEqual(msg1, msg2)
        self.assertEqual(len(shared_hmac), 2)
        
        hmac1 = create.create(msg1, self.key)
        hmac2 = create.create(msg2, self.key)
        self.assertEqual(hmac1[:2], hmac2[:2])


if __name__ == "__main__":
    unittest.main()