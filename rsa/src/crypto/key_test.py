import unittest

from crypto import key
from crypto import primes

# PYTHONPATH=../ python3 key_test.py


class TestKeyAlgorithms(unittest.TestCase):
    def test_key_gen(self):
        p = primes.get_prime(1024)
        q = primes.get_prime(1024)

        public_key, private_key = key.generate(p, q)

        self.assertEqual(public_key[1], p * q)
        self.assertEqual(private_key[1], p * q)

        print("public key: ", public_key[0])
        print("private key: ", private_key[0])


if __name__ == "__main__":
    unittest.main()
