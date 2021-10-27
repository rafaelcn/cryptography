import sys
import argparse

from crypto import key
from crypto import cipher

from ioi import io


def create_parser():
    """
    Creates a parser program
    """
    parser = argparse.ArgumentParser(description='RSA Algorithm')

    parser.add_argument('--encrypt', '-e', action='store_true', help='encrypt'
                        + ' data')
    parser.add_argument('--decrypt', '-d', action='store_true', help='decrypt'
                        + ' data')
    parser.add_argument('--gen-key-pair', '-g', action='store_true',
                        help='generates the public/private key pair to use in'
                        + ' the encryption and decryption')
    parser.add_argument('--key', '-k', help='A public of private key used to'
                        + ' encrypt or decrypt data (depends on your wish)')
    parser.add_argument('--file', '-f', type=list, help='files to be encrypted'
                        + ' or decrypted given a key')
    parser.add_argument('--verify', '-v', type=list, help='verify a signature')
    parser.add_argument('--sign', '-s', type=list, help='make a signature')

    return parser


def main():

    parser = create_parser().parse_args()

    if (parser.file is None):
        parser.usage()
        sys.exit(0)

    if (parser.gen_key_pair):
        # generate key pair and save it on the local disk
        pub_key = {}
        prv_key = {}

        pub_key, prv_key = key.generate()

        io.write_key(prv_key, 'key')
        io.write_key(pub_key, 'key.pub')

    if (parser.encrypt):
        if (parser.key is None):
            print('missing -key parameter for encryption (a public key '
                  + 'filename)')
            sys.exit(1)

        pub_key = io.read_key(parser.key)

        for file in parser.file:
            data = io.read(file)
            cipher.encrypt(data, pub_key)

    elif (parser.decrypt):
        if (parser.key is None):
            print('missing -key parameter for decryption (a private key '
                  + 'filename)')
            sys.exit(1)

        prv_key = io.read_key(parser.key)

        for file in parser.file:
            data = io.read(file)
            cipher.decrypt(data, prv_key)


if __name__ == '__main__':
    main()
