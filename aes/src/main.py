import os
import math
import hashlib
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
    p.add_argument('-c', '--cycles', help='number of encryption cycles',
                   default=5, type=int, required=False)

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

    print('key with {} bytes'.format(key_size))
    print('image with {} bytes, creating {} blocks'.format(len(data),
          data_block_size))

    key_block = bytes(parser.key, 'utf-8')

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'\x00' * quantity

    # fill the data with zeros if it's not a multiple of the block size
    if len(data) % parser.block_size != 0:
        quantity = parser.block_size - (len(data) % parser.block_size)
        data += b'\x00' * quantity

    cryptogram = ""
    file_extension = os.path.splitext(parser.input)[1]
    alg = ecb.ECB(key_block) if parser.modes == 'ecb' else ctr.CTR(key_block, os.urandom(16))

    hashes = []
    hasher = hashlib.sha256()

    for i in range(parser.cycles):
        if i == 0:
            cryptogram = alg.encrypt(data)
        else:
            cryptogram = alg.encrypt(cryptogram)

        hasher.update(cryptogram)
        hashes.append(hasher.hexdigest())

        # write the cryptogram to a file along with its decrypted counterpart.
        with open(parser.output+str(i), 'wb') as f:
                f.write(cryptogram)

        with open(parser.output+str(i)+file_extension, 'wb') as f:
            f.write(alg.decrypt(cryptogram))

    # write hashes of the cryptogram to a file
    with open(parser.output+'_hashes.txt', 'w') as f:
        for h in hashes:
            f.write('- '+h+'\n')


if __name__ == "__main__":
    main()
