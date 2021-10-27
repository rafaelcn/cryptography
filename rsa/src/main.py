import sys
import base64
import argparse

from crypto import key
from crypto import primes
from crypto import cipher
from crypto import certificate

from ioi import io


def create_parser():
    """
    Creates a parser program
    """
    parser = argparse.ArgumentParser(description='RSA Algorithm')

    parser.add_argument('-e', '--encrypt' , help='encrypt data', default=False, 
                        action='store_true')
    parser.add_argument('-d', '--decrypt' , help='decrypt data', default=False, 
                        action='store_true')

    parser.add_argument('-g', '--gen-key-pair' , default=False, 
                        action='store_true',
                        help='generates the public/private key pair to use in'
                        + ' the encryption and decryption')

    parser.add_argument('-k', '--key' , help='A public of private key used to'
                        + ' encrypt or decrypt data (depends on your wish)')
    parser.add_argument('-f', '--file', help='file to be encrypted  or '
                        + 'decrypted given a key')

    parser.add_argument('-v', '--verify' , type=list, help='verify a signature')
    parser.add_argument('-s', '--sign' , type=list, help='make a signature')

    return parser


def main():

    parser = create_parser().parse_args()

    if (parser.gen_key_pair):
        # generate key pair and save it on the local disk
        pub_key = {}
        prv_key = {}

        p = primes.get_random_bits(1024)
        q = primes.get_random_bits(1024)

        pub_key, prv_key = key.generate(p, q)

        io.write_key('key', prv_key)
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

            data = io.read(parser.file)
            encrypted_data = cipher.encrypt(data, pub_key)

            io.write_cryptogram(parser.file + ".enc", encrypted_data)

        elif (parser.decrypt):
            prv_key = io.read_key(parser.key)

            for file in parser.file:
                data = io.read(file)
                cipher.decrypt(data, prv_key)
    elif (parser.sign):
        pub_key = {}
        prv_key = {}

        # read a private and a .pub key and certificate data from sign
        for argument in parser.sign:
            if (argument.endswith('.pub')):
                pub_key = io.read_key(argument)
            

        certificate.sign()
    elif (parser.verify):
        pass


if __name__ == '__main__':
    main()
