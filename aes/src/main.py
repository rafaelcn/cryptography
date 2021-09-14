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

    # print("parser.key: ",parser.key)
    # print("parser.key.len: ",len(parser.key))
    print(parser.block_size)
    print(parser.modes)
    print(parser.input)

    with open(parser.input, 'rb') as f:
        data = f.read()

    key_size = len(parser.key)
    print("key_size: ", key_size)
    block_size = math.ceil(len(data) / parser.block_size)

    print('image with {} bytes, creating {} blocks...'.format(len(data),
          block_size))
    print('key with {} bytes'.format(key_size))

    key_block = bytes(parser.key, 'utf-8')
    #print("key_block_len:",len(key_block))

    # fill the key with zeros
    if key_size < parser.block_size:
        quantity = parser.block_size - key_size
        #print("quantity", quantity)
        key_block += b'\x00' * quantity

    # fill the data with zeros if it's not a multiple of the block size
    if len(data) % parser.block_size != 0:
      quantity = parser.block_size - (len(data) % parser.block_size)
      data += b'\x00' * quantity
    print(len(key_block))
    print(len(data))
    # for i, k in data_blocks.items():
    #   print("block {}".format(i), k, "\n\n")
    #
    # print("key", key_block)
    # print(len(key_block))
    if parser.modes == 'ecb':
        import aes_ecb
        key = key_block
        encrypted = aes_ecb.AES(key).encrypt_block(data)
        fin = open('github_profile_copy.png', 'wb')
        # writing encrypted data in image
        fin.write(encrypted)
        fin.close()
        print('Encryption Done...')
        decrypted = aes_ecb.AES(key).decrypt_block(encrypted)
        fin = open('github_profile_copy.png', 'wb')
        
        # writing decryption data in image
        fin.write(decrypted)
        fin.close()
        print('Decryption Done...')
    if parser.modes == 'ctr':
        # ctr mode
        import aes_ctr
        import os
        key = key_block
        
        iv = os.urandom(128)
        # print(iv)
        encrypted = aes_ctr.AES(key).encrypt_ctr(data, iv)
        # converting image into byte array to
        # perform encryption easily on numeric data
        fin = open('github_profile_copy.png', 'wb')
        # writing encrypted data in image
        fin.write(encrypted)
        fin.close()
        print('Encryption Done...')
        #encrypted = aes.AES(key).encrypt_ctr(, iv)
        #print(encrypted)
        print(len(encrypted))
        decrypted = aes_ctr.AES(key).decrypt_ctr(encrypted, iv)
        fin = open('github_profile_copy.png', 'wb')
        
        # writing decryption data in image
        fin.write(decrypted)
        fin.close()
        print('Decryption Done...')


if __name__ == "__main__":
    main()
