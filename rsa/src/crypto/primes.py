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
        if primarity_test(candidate):
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


def primarity_test(mrc, iterations=20):
    """
    Runs iterations number of times of the Rabin Miller primality test.
    """
    max_divisions = 0
    ec = mrc - 1

    while ec % 2 == 0:
        ec >>= 1
        max_divisions += 1
        assert(2**max_divisions * ec == mrc - 1)

        def trial(round_tester):
            if pow(round_tester, ec, mrc) == 1:
                return False

            for i in range(max_divisions):
                if (pow(round_tester, 2**i * ec, mrc) == mrc - 1):
                    return False

            return True

        for _ in range(iterations):
            round_tester = random.randrange(2, mrc)
            if trial(round_tester):
                return False

    return True
