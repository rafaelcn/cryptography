import math
import argparse


def create_parser():
    p = argparse.ArgumentParser(description='AES')

    p.add_argument('-k', '--key', help='key', required=True)
    p.add_argument('-i', '--input', help='input file', required=True)
    p.add_argument('-o', '--output', help='output file', required=False)
    p.add_argument('-s', '--block-size', help='block size', default=128,
                   type=int, required=False)
    p.add_argument('-m', '--modes', help='AES modes of operation',
                   default='ecb', choices=['ecb', 'ctr'], required=False)

    return p


def main():

    parser = create_parser().parse_args()

    if parser.output is None:
        parser.output = parser.input + '.enc'

    data = ""

    print(parser.key)
    print(parser.block_size)
    print(parser.modes)
    print(parser.input)

    with open(parser.input, 'rb') as f:
        data = f.read()

    key_size = len(parser.key)
    block_size = math.ceil(len(data) / parser.block_size)

    print('image with {} bytes, creating {} blocks...'.format(len(data),
          block_size))
    print('key with {} bytes'.format(key_size))

    key_block = bytes(parser.key, 'utf-8')

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'\x00' * quantity

    # fill the data with zeros if it's not a multiple of the block size
    if len(data) % parser.block_size != 0:
        quantity = parser.block_size - (len(data) % parser.block_size)
        data += b'\x00' * quantity

    # for i, k in data_blocks.items():
    #    print("block {}".format(i), k, "\n\n")
    #
    # print("key", key_block)

    if parser.modes == 'ecb':
        from cypher_ecb import AES_ECB
        #cypher.encrypt(data_blocks, key_block)
        AES_ECB.encrypt(bytearray(data), key_block)


if __name__ == "__main__":
    main()