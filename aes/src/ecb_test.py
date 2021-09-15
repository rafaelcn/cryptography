import os
import unittest
import hashlib

from aes import ecb

from Crypto.Cipher import AES


class TestECBAlgorithm(unittest.TestCase):
    def test_enc(self):
        keys = [b'somethingwith323']
        data = [os.urandom(16*(2**i)) for i in range(1, 8)]

        for key in keys:
            alg = ecb.ECB(key)
            cipher = AES.new(key, AES.MODE_ECB)

            for d in data:
                c1, c2 = alg.encrypt(d), cipher.encrypt(d)

                h1 = hashlib.sha256()
                h1.update(c1)

                h2 = hashlib.sha256()
                h2.update(c2)

                self.assertEqual(h1.hexdigest(), h2.hexdigest())


if __name__ == '__main__':
    unittest.main()