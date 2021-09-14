import os
import math
import argparse

from aes import ecb, ctr


def create_parser():
    p = argparse.ArgumentParser(description='AES')

    p.add_argument('-k', '--key', help='key', required=True)
    p.add_argument('-i', '--input', help='input file', required=True)
    p.add_argument('-o', '--output', help='output file', required=False)
    p.add_argument('-s', '--block-size', help='block size in bytes',
                   default=16, type=int, required=False)
    p.add_argument('-m', '--modes', help='AES modes of operation',
                   default='ecb', choices=['ecb', 'ctr'], required=False)

    return p


def main():

    parser = create_parser().parse_args()

    if parser.output is None:
        parser.output = parser.input + '.enc'

    data = ""

    print("{}".format(parser.block_size))
    print("{}".format(parser.modes))
    print("{}".format(parser.input))

    with open(parser.input, 'rb') as f:
        data = f.read()

    key_size = len(parser.key)
    data_block_size = math.ceil(len(data) / parser.block_size)

    print('image with {} bytes, creating {} blocks'.format(len(data),
          data_block_size))
    print('key with {} bytes, filling with zeros'.format(key_size))

    key_block = bytes(parser.key, 'utf-8')

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'\x00' * quantity

    # fill the data with zeros if it's not a multiple of the block size
    if len(data) % parser.block_size != 0:
        quantity = parser.block_size - (len(data) % parser.block_size)
        data += b'\x00' * quantity

    if parser.modes == 'ecb':
        alg = ecb.ECB(key_block)

        cryptogram = alg.encrypt(data)

        with open(parser.output, 'wb') as f:
            f.write(cryptogram)

        with open(parser.output+".png", 'wb') as f:
            f.write(alg.decrypt(cryptogram))

    elif parser.modes == 'ctr':
        alg = ctr.CTR(key_block, os.urandom(128))

        cryptogram = alg.encrypt(key_block)

        with open(parser.output, 'wb') as f:
            f.write(cryptogram)

        with open(parser.output+".png", 'wb') as f:
            f.write(alg.decrypt(cryptogram))


if __name__ == "__main__":
    main()
