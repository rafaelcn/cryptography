import unittest

from crypto import key
from crypto import primes
from crypto import certificate

# PYTHONPATH=. python3 src/certificate_test.py (on src)
# PYTHONPATH=../ python3 certificate_test.py (on crypto)


class TestKeyAlgorithms(unittest.TestCase):
    def test_sign_and_validation(self):
        p = primes.get_random_bits(1024)
        q = primes.get_random_bits(1024)

        msg = b"Rafael e Rafael fazem um trabalho com cara de pastel"

        public_key, private_key = key.generate(p, q)

        signature = certificate.sign(msg, private_key, public_key)

        self.assertTrue(certificate.validate(msg, signature, public_key))


if __name__ == "__main__":
    unittest.main()
