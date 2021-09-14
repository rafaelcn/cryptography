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

    data_blocks = {}
    key_block = bytes(parser.key, 'utf-8')

    for i in range(block_size):
        data_blocks[i] = [data[i * parser.block_size:(i + 1) * parser.block_size]]

    # fill the last block with zeros
    if len(data) % parser.block_size != 0:
        quantity = parser.block_size - len(data_blocks[block_size - 1][0])
        data_blocks[block_size - 1].append(b'\x00' * quantity)

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'\x00' * quantity

    # for i, k in data_blocks.items():
    #    print("block {}".format(i), k, "\n\n")
    #
    # print("key", key_block)

    if parser.modes == 'ecb':
        from aes import cypher
        cypher.encrypt(data_blocks, key_block, data_blocks)


if __name__ == "__main__":
    main()
