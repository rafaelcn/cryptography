import random


primes_table = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103,
    107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179,
    181, 191, 193, 197, 199, 211, 223,
    227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293,
    307, 311, 313, 317, 331, 337, 347,
    349, 353, 359, 367, 373, 379, 383,
    389, 397, 401, 409, 419, 421, 431,
    433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499, 503, 509,
]


def _get_random_number(interval):
    """
        Get a random number in the interval.
    """
    return random.randrange(2**(interval-1), 2**interval - 1)


def get_random_bits(size=1024):
    """
    Get a  random number with size bits that is a good candidate and
    passes the primarity test.
    """
    while True:
        candidate = _get_random_number(size)
        if primarity_test(candidate):
            return candidate


def get_prime(size=1024):
    """
        Generate a prime candidate divisible by the first primes of the table.
    """
    while True:
        candidate = _get_random_number(1024)
        for prime in primes_table:
            if candidate % prime == 0 and prime**2 <= candidate:
                break
            else:
                return candidate


def primarity_test(mrc, iterations=20):
    """
        Runs iterations number of times of the Rabin Miller primality test.
    """
    if mrc < 2:
        return False
    if mrc in primes_table:
        return True
    if mrc % 2 == 0:
        return False
    s = mrc - 1
    while s % 2 == 0:
        s >>= 1
    for _ in range(iterations):
        a = random.randrange(2, mrc - 1)
        v = pow(a, s, mrc)
        if v != 1:
            i = 0
            while v != mrc - 1:
                if i == s - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % mrc
    return True
