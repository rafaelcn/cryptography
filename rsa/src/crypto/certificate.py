from crypto import cipher


def sign(data_hash, private_key, public_key):
    """
    Sign (certificate) a piece of data hash.
    """
    signature = pow(cipher.os2ip(data_hash), private_key['d'], public_key['n'])
    signature = cipher.i2osp(signature, 1024)

    return signature


def validate(data_hash, signature, public_key):
    """
    Validate a signature from a data hash.
    """
    validation = cipher.os2ip(signature)
    validation = pow(signature, public_key['e'], public_key['n'])
    validation = cipher.i2osp(validation, 32)

    if validation == data_hash:
        return True

    return False
