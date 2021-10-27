from crypto import hash
from crypto import cipher


def sign(data, private_key, public_key):
    """
    Sign (certificate) a piece of data hash and return it.
    """
    signature = pow(cipher.os2ip(data), private_key['d'], public_key['n'])
    signature = cipher.i2osp(signature, 1024)

    return signature


def validate(data, signature, public_key):
    """
    Checks wheter or not a signature is really signed with the given public
    key.
    """
    hashed = hash.hashit(data)

    validation = pow(cipher.os2ip(signature), public_key['e'], public_key['n'])
    validation = cipher.i2osp(validation, 32)

    if validation == hashed:
        return True

    return False
