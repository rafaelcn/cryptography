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

        for size, number in d.items():
            print(f'{number} - {size}\n\n')

    def test_primarity_test(self):
        self.assertTrue(primes.primarity_test(2))
        self.assertFalse(primes.primarity_test(6))
        self.assertTrue(primes.primarity_test(7))
        self.assertTrue(primes.primarity_test(11))
        self.assertFalse(primes.primarity_test(121))
        self.assertFalse(primes.primarity_test(1))


if __name__ == "__main__":
    unittest.main()
