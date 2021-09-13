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
    #print(data)


if __name__ == "__main__":
    main()
