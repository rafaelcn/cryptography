import math
import random

from crypto.utils import gcde
from crypto.primes import get_prime, get_random_bits


def _key_size(size=1024):
    """
        Verifies if a prime candidate for the key size is a good key fit.
    """
    while True:
        candidate = get_prime(size)


def key_gen(p, q):
    """
        Generates a public and private key pair
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, phi - 1)
        if math.gcd(e, phi) == 1:
            u, s, t = gcde(e, phi)
        if u == (s * phi + t * e):
            d = t % phi
            break

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key
