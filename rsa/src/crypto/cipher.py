"""
Actually contains the functions responsible for encryption and decryption using
the RSA algorithm.
"""

import math
import random
import string

from crypto import hash


def mgf1(input: bytes, mlen: int, f_hash=hash.hashit):
    """
    Mask generation function
    """
    t = b''
    hlen = len(f_hash(b''))
    for c in range(0, math.ceil(mlen/hlen)):
        temp_c = c.to_bytes(4, byteorder="big")
        t += f_hash(input + temp_c)

    return t[:mlen]


def xor(data: bytes, mask: bytes):
    """
    XORs two byte strings together
    """
    return bytes([_a ^ _b for _a, _b in zip(data, mask)])


def os2ip(x: bytes):
    """
    Converts a byte string to an integer
    """
    return int.from_bytes(x, byteorder='big', signed=False)


def i2osp(x: int, length: int):
    """
    Converts an integer to a byte string of a specified length
    """
    return x.to_bytes(length, byteorder='big', signed=False)


def oaep_encode(m: string, n: int, k0: int, k1: int):
    """
    Padding scheme OAEP used before encryption
    """
    # 1) Add k1 zeros to the message
    for i in range(k1):
        m += str(0)

    # 2) Gera um r aleatório de tamanho k0
    src = string.ascii_lowercase + string.digits
    r = ''.join(random.SystemRandom().choice(src) for _ in range(k0))

    # 3) Usa o oráculo G = mgf1 para expandir r de k0 para n - k0 de tamanho
    expanded = mgf1(bytes(r, "utf-8"), n - k0)

    # 4) XOR bytes with the expanded r
    x = xor(bytes(m, "utf-8"), expanded)
    y = xor(bytes(r, "utf-8"), hash.hashit(x))

    # 5) Concat the result bytes from step 4)
    result = b''.join([x, y])

    return x, y, result


def oaep_decode(x: bytes, y: bytes, n=1024, padding=32):
    """
    """
    r = xor(y, hash.hashit(x))
    m = xor(x, mgf1(r, n - padding))

    # for clearer output we transform the bytes to string and remove any
    # inserted zero characters.
    m = str(m, 'utf-8')
    m = str(m).replace("0", "")

    return r, m


def encrypt(msg, public_key: dict):
    """
    Encrypts a message using the public key tuple containing n and e
    """
    x, y, m = oaep_encode(msg, 1024, 32, 16)

    c = pow(os2ip(m), public_key['e'], public_key['n'])
    return c, len(m), len(x), len(y)


def decrypt(data: tuple, private_key: dict):
    """
    Decrypts a message using the private key tuple containing n and d
    """
    m = pow(data[0], private_key['d'], private_key['n'])

    message_size = data[1]

    x = data[2]
    y = data[3]

    bytes = i2osp(m, message_size)
    message = oaep_decode(bytes[:x], bytes[x:x + y])

    return message[1]
