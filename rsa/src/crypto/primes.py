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
    Get a random number in the defined interval.
    """
    return random.randrange(2**(interval-1), 2**interval - 1)


def get_random_bits(size=1024):
    """
    Get a  random number with size bits that is a good candidate and
    passes the primarity test.
    """
    while True:
        candidate = get_prime(size)
        if primality(candidate):
            return candidate


def get_prime(size=1024):
    """
    Generate a prime candidate coprime with the first primes of the table.
    """
    while True:
        candidate = _get_random_number(size)
        for prime in primes_table:
            if candidate % prime == 0 and prime**2 <= candidate:
                break
            else:
                return candidate


def primality(n: int, iterations=40):
    """
    Runs iterations number of times of the Rabin Miller primality test and
    returns whether or not a number n is a possible prime.

    Why 40 rounds as a default? The answer lies below.
    https://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    """

    if n == 2:
        return True

    if n % 2 == 0 or n == 1:
        return False

    r = 0
    s = n - 1

    while s % 2 == 0:
        r += 1
        s >>= 1

    for _ in range(iterations):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True
