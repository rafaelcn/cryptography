import argparse


def create_parser():
    """
    """
    parser = argparse.ArgumentParser(description='RSA Algorithm')

    parser.add_argument('--encrypt', '-e', action='store_true', help='encrypt'
                        + ' data')
    parser.add_argument('--decrypt', '-d', action='store_true', help='decrypt'
                        + ' data')
    parser.add_argument('--file', '-f', type=list, help='files to be encrypted'
                        + ' or decrypted')

    return parser


def main():

    parser = create_parser()
    parser.parse_args()

    if (parser.file is None):
        print('No files specified')
        return

    if (parser.encrypt):
        encrypt(parser.file)
    elif (parser.decrypt):
        decrypt(parser.file)


def encrypt(files):
    pass


def decrypt(files):
    pass


if __name__ == '__main__':
    main()
