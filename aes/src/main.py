import argparse


def init_parser():
    p = argparse.ArgumentParser(description='AES')

    p.add_argument('-k', '--key', help='key', required=True)
    p.add_argument('-i', '--input', help='input file', required=True)
    p.add_argument('-o', '--output', help='output file', required=False)
    p.add_argument('-m', '--modes', help='AES modes of operation',
                   required=False, default='ecb,ctr')

    return p


def main():

    parser = init_parser().parse_args()

    if parser.output is None:
        parser.output = parser.input + '.enc'

    data = ""

    with open(parser.input, 'rb') as f:
        data = f.read()

    print(data)


if __name__ == "__main__":
    main()
