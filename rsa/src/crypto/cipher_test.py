import unittest

from crypto import key
from crypto import primes
from crypto import cipher

# PYTHONPATH=. python3 src/cipher_test.py (on src)
# PYTHONPATH=../ python3 cipher_test.py (on crypto)


class TestKeyAlgorithms(unittest.TestCase):
    def test_key_gen(self):
        p = primes.get_random_bits(1024)
        q = primes.get_random_bits(1024)

        msg = 'Rafael e Rafael fazem um trabalho com cara de pastel'

        public_key, private_key = key.generate(p, q)

        self.assertEqual(public_key['n'], p * q)
        self.assertEqual(private_key['n'], p * q)

        encrypted_message, t, x, y = cipher.encrypt(msg, public_key)

        decrypted_message = cipher.decrypt(encrypted_message, private_key,
                                           t, x, y)

        self.assertEqual(decrypted_message, msg)


if __name__ == "__main__":
    unittest.main()
