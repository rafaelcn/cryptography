import unittest

from crypto import primes

# PYTHONPATH=. python3 crypto/primes_test.py (on src)
# PYTHONPATH=../ python3 primes_test.py (on src/crypto)


class TestPrimesAlgorithms(unittest.TestCase):
    def test_get_prime(self):

        d = {
            1024: primes.get_prime(1024),
            2048: primes.get_prime(2048),
        }

        self.assertLessEqual(len(str(d[1024])), 1024)
        self.assertLessEqual(len(str(d[2048])), 2048)

    def test_primarity(self):
        self.assertTrue(primes.primality(2))
        self.assertFalse(primes.primality(6))
        self.assertTrue(primes.primality(7))
        self.assertTrue(primes.primality(11))
        self.assertFalse(primes.primality(121))
        self.assertFalse(primes.primality(1))


if __name__ == "__main__":
    unittest.main()
