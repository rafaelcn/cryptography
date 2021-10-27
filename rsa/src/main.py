import sys
import base64
import argparse

from crypto import key
from crypto import hash
from crypto import primes
from crypto import cipher
from crypto import certificate

from ioi import io


def create_parser():
    """
    Creates a parser program
    """
    parser = argparse.ArgumentParser(description='RSA Algorithm')

    parser.add_argument('-e', '--encrypt', help='encrypt data', default=False,
                        action='store_true')
    parser.add_argument('-d', '--decrypt', help='decrypt data', default=False,
                        action='store_true')

    parser.add_argument('-g', '--gen-key-pair', default=False,
                        action='store_true',
                        help='generates the public/private key pair to use in'
                        + ' the encryption and decryption')

    parser.add_argument('-k', '--key', help='A public or private key used to'
                        + ' encrypt or decrypt data (depends on your wish)')
    parser.add_argument('-f', '--file', help='file to be encrypted  or '
                        + 'decrypted given a key')

    parser.add_argument('-v', '--verify', nargs='+', help='verify a signature')
    parser.add_argument('-s', '--sign', nargs='+', help='make a signature for '
                        + 'a given file')

    return parser


def main():

    parser = create_parser().parse_args()

    if (parser.gen_key_pair):
        # generate key pair and save it on the local disk
        pub_key = {}
        prv_key = {}

        print('Generating public and private keys...')

        p = primes.get_random_bits(1024)
        q = primes.get_random_bits(1024)

        pub_key, prv_key = key.generate(p, q)

        io.write_key('key.prv', prv_key)
        io.write_key('key.pub', pub_key)

    if parser.encrypt or parser.decrypt:
        if parser.file is None:
            # print program usage
            print("Usage: python3 main.py -e/d -f <file> -k <key>")
            sys.exit(1)

        if (parser.key is None):
            print('missing -key parameter for encryption/decryption')
            sys.exit(1)

        pub_key = {}
        prv_key = {}

        if (parser.encrypt):
            pub_key = io.read_key(parser.key)

            filename = io.read(parser.file)
            encrypted_data = cipher.encrypt(filename, pub_key)

            io.write_cryptogram(parser.file + ".enc", encrypted_data)

        elif (parser.decrypt):
            prv_key = io.read_key(parser.key)

            for file in parser.file:
                filename = io.read(file)
                cipher.decrypt(filename, prv_key)
    elif (parser.sign):
        pub_key = {}
        prv_key = {}

        filename = ''

        # read a private and a public key and certificate data from sign

        for arg in parser.sign:
            if arg.endswith('.pub'):
                pub_key = io.read_key(arg)
            elif arg.endswith('.prv'):
                prv_key = io.read_key(arg)
            else:
                filename = arg

        print(f'Signing file {filename} with keys...')

        text = io.read(filename)
        hashed = hash.hashit(bytes(text, 'utf-8'))

        signature = certificate.sign(hashed, prv_key, pub_key)

        encoded = base64.b64encode(signature)

        io.write(filename + ".sig", str(encoded, 'utf-8'))
    elif (parser.verify):
        pub_key = {}

        filename = ''
        signature = ''

        for arg in parser.verify:
            if arg.endswith('.pub'):
                pub_key = io.read_key(arg)
            elif arg.endswith('.sig'):
                signature = io.read(arg)
            else:
                filename = arg

        text = bytes(io.read(filename), 'utf-8')
        decoded_signature = base64.b64decode(signature)

        validation = certificate.validate(text, decoded_signature, pub_key)

        if validation:
            print('Signature is valid')
        else:
            print('Signature is invalid')


if __name__ == '__main__':
    main()
