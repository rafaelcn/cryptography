import os
import unittest
import hashlib

from aes import ecb
from image import StrippedImage

from PIL import Image
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

    def test_enc_crypto(self):
        """
        Test made to output the correct encrypted version of a given image.
        """
        key = b'somethingwith323'
        cipher = AES.new(key, AES.MODE_ECB)
        filepath = '../assets/self.bmp'

        image = StrippedImage(os.path.join(os.path.dirname(__file__),
                              filepath))

        if image.size % 16 != 0:
            quantity = 16 - (image.size % 16)
            image.body += b'~' * quantity

        c = cipher.encrypt(image.body)

        encrypted_image = Image.frombytes("RGB",
                                          image.resolution,
                                          image.header+c)
        encrypted_image.save("test-aes-ecb"+".bmp")


if __name__ == '__main__':
    unittest.main()
