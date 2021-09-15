import os
import math
import hashlib
import argparse

from PIL import Image

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
                   default=1, type=int, required=False)
    p.add_argument('-r', '--rounds', help='number of encryption rounds ' +
                   '(depends on block size)', default=10, type=int,
                   required=False)
    p.add_argument('-v', '--initialization-vector', help='initialization ' +
                   'vector of the CTR mode (default os.urandom(16))',
                   default=os.urandom(16), type=bytes)

    return p


def main():

    parser = create_parser().parse_args()

    if parser.output is None:
        parser.output = parser.input + '.enc'

    data = ""
    image = None

    print("block size: {}".format(parser.block_size))
    print("operation mode: {}".format(parser.modes))
    print("input file: {}".format(parser.input))

    #with open(parser.input, 'rb') as f:
    #    data = f.read()

    with Image.open(parser.input) as im:
        image = im
        data = im.tobytes()

    key_size = len(parser.key)
    data_block_size = math.ceil(len(data) / parser.block_size)

    print('key size {} bytes'.format(key_size))
    print('image size {} bytes, creating {} blocks'.format(len(data),
          data_block_size))

    key_block = bytes(parser.key, 'utf-8')

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        key_block += b'~' * quantity

    # fill the data with zeros if it's not a multiple of the block size
    if len(data) % parser.block_size != 0:
        quantity = parser.block_size - (len(data) % parser.block_size)
        data += b'~' * quantity

    cryptograms = []
    file_extension = os.path.splitext(parser.input)[1]

    # if the initialization vector is random, the output for the same image
    # might change as a result of that.
    alg = None

    if parser.modes == 'ecb':
        alg = ecb.ECB(key_block, parser.rounds)
    else:
        alg = ctr.CTR(key_block, parser.initialization_vector, parser.rounds)

    hashes = []

    for i in range(parser.cycles):
        if i == 0:
            cryptograms.append(alg.encrypt(data))
        else:
            cryptograms.append(alg.encrypt(cryptograms[i-1]))

        # initialize hashlib at each cycle to prevent shadowing.
        hasher = hashlib.sha256()
        hasher.update(cryptograms[i])

        hashes.append(hasher.hexdigest())

        #print(len(data), len(cryptograms[i]))
        #im = Image.frombytes("RGB", [400, 400], cryptograms[i])
        #im.show()

        with open(parser.output+"-"+str(i), 'wb') as f:
                f.write(cryptograms[i])

        im = Image.frombytes("RGB", [400, 400], alg.decrypt(cryptograms[i]))
        #f.write(alg.decrypt(cryptograms[i]))
        im.save(parser.input+".dec-"+str(i)+file_extension)

    # write hashes of the cryptogram to a file
    with open(parser.input+'_hashes.txt', 'w') as f:
        for h in hashes:
            f.write('- '+h+'\n')

    image.close()

if __name__ == "__main__":
    main()
