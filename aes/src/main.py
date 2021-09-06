import argparse


def parser():
    p = argparse.ArgumentParser(description='AES')

    p.add_argument('-k', '--key', help='key', required=True)
    p.add_argument('-i', '--input', help='input file', required=True)
    p.add_argument('-o', '--output', help='output file', required=False)

    return p


def main():

    p = parser().parse_args()

    if p.output is None:
        p.output = p.input + '.enc'

    data = ""

    with open(p.input, 'rb') as f:
        data = f.read()

    print(data)


if __name__ == "__main__":
    main()
