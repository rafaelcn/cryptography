import unittest
import tempfile

from ioi import io

class TestKeyAlgorithms(unittest.TestCase):
    def test_read_key(self):
        # write a temp key in the temp folder of the OS and read it
        key_1 = {'n': 1024, 'e': 3239817237812367123718232}

        with tempfile.TemporaryFile(mode='r+') as file:
            file.write(f'{key_1}')
            file.seek(0)

            data = io.read_key(file.name)

            self.assertEqual(data, key_1)
    


if __name__ == "__main__":
    unittest.main()

