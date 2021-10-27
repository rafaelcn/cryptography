"""
This file contains hash functions to help in signature verfication.
"""

import hashlib


def hashit(data):
    """
    Hash function that returns a 32 byte digest of the application of SHA3 256
    on data.
    """
    return hashlib.sha3_256(data).digest()
