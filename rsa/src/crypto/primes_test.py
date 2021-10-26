import unittest

from crypto import primes

# PYTHONPATH=../ python3 primes_test.py


class TestPrimesAlgorithms(unittest.TestCase):
    def test_get_prime(self):

        d = {
            1024: primes._get_random_number(1024),
            2048: primes._get_random_number(2048),
        }

        for size, number in d.items():
            print(f'{number} - {size}\n\n')


if __name__ == "__main__":
    unittest.main()