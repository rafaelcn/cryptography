import unittest
import tempfile

from ioi import io


class TestKeyAlgorithms(unittest.TestCase):
    def test_read_key(self):
        key_1 = {'n': 1024, 'e': 3239817237812367123718232}

        file = tempfile.TemporaryFile(mode='r+')

        file.write(f'{key_1}')
        file.seek(0)

        data = io.read_key(file.name)

        # TODO: fix error of file not being closed...
        self.assertEqual(data, key_1)


if __name__ == "__main__":
    unittest.main()
