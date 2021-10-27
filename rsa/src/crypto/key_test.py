import unittest

from crypto import key
from crypto import primes

# PYTHONPATH=. python3 crypto/key_test.py (on src)
# PYTHONPATH=../ python3 key_test.py (on src/crypto)


class TestKeyAlgorithms(unittest.TestCase):
    def test_key_gen(self):
        p = primes.get_prime(1024)
        q = primes.get_prime(1024)

        public_key, private_key = key.generate(p, q)

        self.assertEqual(public_key['n'], p * q)
        self.assertEqual(private_key['n'], p * q)

        self.assertTrue(len(str(private_key['d'])) > 0)
        self.assertTrue(len(str(public_key['e'])) > 0)


if __name__ == "__main__":
    unittest.main()
