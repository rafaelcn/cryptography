import os
import math
import hashlib
import argparse

from PIL import Image

from image import StrippedImage
from aes import ecb, ctr


def create_parser():
    """
    Creates a parser with the given arguments.
    """
    p = argparse.ArgumentParser(description='AES')

    p.add_argument('-k', '--key', help='key', required=True)
    p.add_argument('-i', '--input', help='input file', required=True)
    p.add_argument('-o', '--output', help='output file', required=False)
    p.add_argument('-s', '--block-size', help='block size in bytes',
                   default=16, type=int, required=False)
    p.add_argument('-m', '--modes', help='AES modes of operation',
                   default='ecb', choices=['ecb', 'ctr'], required=False)
    p.add_argument('-c', '--cycles', help='number of encryption cycles',
                   default=1, type=int, required=False)
    p.add_argument('-r', '--rounds', help='number of encryption rounds ' +
                   '(depends on block size)', default=10, type=int,
                   required=False)
    p.add_argument('-v', '--initialization-vector', help='initialization ' +
                   'vector of the CTR mode (default os.urandom(16))',
                   default=os.urandom(16), type=bytes)
    p.add_argument('-vvv', '--verbose', help='verbose mode', default=False)

    return p


def main():

    parser = create_parser().parse_args()

    if parser.output is None:
        parser.output = os.path.splitext(parser.input)[0] + '.enc'

    print("block size: {}".format(parser.block_size))
    print("operation mode: {}".format(parser.modes))
    print("input file: {}".format(parser.input))

    # read the input file (a bitmap image)
    image = StrippedImage(parser.input)

    key_size = len(parser.key)
    data_block_size = math.ceil(image.size / parser.block_size)

    print('key size {} bytes'.format(key_size))
    print('image size {} bytes, creating {} blocks'.format(image.size,
          data_block_size))

    key_block = bytes(parser.key, 'utf-8')

    # fill the key block with ~ if it is not long enough, respective to the
    # block size.
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'~' * quantity

    # fill the data with ~ if it's not a multiple of the block size
    if image.size % parser.block_size != 0:
        quantity = parser.block_size - (image.size % parser.block_size)
        image.body += b'~' * quantity

    cryptograms = []
    file_extension = os.path.splitext(parser.input)[1]

    alg = None

    if parser.modes == 'ecb':
        alg = ecb.ECB(key_block, parser.rounds)
    else:
        # if the initialization vector is random, the output for the same image
        # might change as a result of that.
        alg = ctr.CTR(key_block, parser.initialization_vector, parser.rounds)

    hashes = []

    for i in range(parser.cycles):
        if i == 0:
            cryptograms.append(alg.encrypt(image.body))
        else:
            cryptograms.append(alg.encrypt(cryptograms[i-1]))

        # initialize hashlib at each cycle to prevent shadowing.
        hasher = hashlib.sha256()
        hasher.update(cryptograms[i])

        hashes.append(hasher.hexdigest())

        encrypted_image = Image.frombytes("RGB",
                                          image.resolution,
                                          image.header+cryptograms[i])
        encrypted_image.save(parser.output+"-"+str(i)+"."+str(parser.modes) +
                             file_extension)

        log("encrypted image {} was created".format(i), parser.verbose)

        decrypted_image = Image.frombytes("RGB", image.resolution,
                                          image.header+alg.decrypt(cryptograms[i]))
        decrypted_image.save(parser.input+".dec-"+str(i)+"." +
                             str(parser.modes)+file_extension)

        log("decrypted image {} was created".format(i), parser.verbose)

    # write hashes of the cryptogram to a file
    with open(parser.input+'_hashes.txt', 'w') as f:
        for h in hashes:
            f.write('- '+h+'\n')


def log(message: str, verbose: bool = False):
    if verbose:
        print(message)


if __name__ == "__main__":
    main()
