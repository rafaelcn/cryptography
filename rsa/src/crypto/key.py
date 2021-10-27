import math
import random

from utils import gcde


def generate(p, q):
    """
    Generates a public and private key pair from two large prime numbers p and
    q.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, phi - 1)
        if math.gcd(e, phi) == 1:
            u, s, t = gcde(phi, e)
            if u == (s * phi + t * e):
                d = t % phi
                break

    public_key = {'e': e, 'n': n}
    private_key = {'d': d, 'n': n}

    return public_key, private_key
