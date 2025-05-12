import random
import argparse
from math import ceil, log10

from gmpy2 import powmod

# first 100 primes
small_primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
    421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
    509, 521, 523, 541
]


def is_divisible_by_small_prime(n):
    """
    condition 1 (Fermat's Little Theorem)
    """
    return any(n % p == 0 for p in small_primes)


def miller_rabin_iteration(n):
    # First, see if n is divisible by one of the first 100 primes
    # Sometimes this will shortcut, and we immediately find n is composite
    if is_divisible_by_small_prime(n) and n > small_primes[-1]:
        return False

    a = _pick_random_base(n)
    e = _start_expoent(n)
    if _fermat_little_theorem(a, e, n):
        return False

    prev_is1 = True
    while _is_even(e):
        e //= 2
        x = powmod(a, e, n)
        if prev_is1:  # condition 2
            if x == n - 1:
                prev_is1 = False
            elif x != 1:
                return False
    return True


def _is_even(e):
    return e % 2 == 0


def _start_expoent(n):
    return n - 1


def _pick_random_base(n):
    return random.randint(2, n - 1)


def _fermat_little_theorem(a, e, n):
    return powmod(a, e, n) != 1


def miller_rabin(n, k):
    # Iterate the Miller-Rabin test k times
    # achieves >= (1 - 0.25^k) confidence
    for _ in range(k):
        if not miller_rabin_iteration(n):
            return False
    return True


def generate_random(num_digits):
    min_n_digit_number = 10 ** (num_digits - 2)
    max_n_digit_number = 10 ** (num_digits - 1) - 1
    last_digit = random.choice([1, 3, 7, 9])
    n = random.randint(min_n_digit_number, max_n_digit_number)
    return n * 10 + last_digit


def generate_prime(num_digits, k=10):
    # generate random numbers with num_digits digits until a prime is found.
    # Expected iterations is O(num_digits) due to the prime number theorem!
    expected = int(2.3 * num_digits)
    for i in range(1, expected):
        print(f"""iteration: {i} (expected <= {expected} total due to PNT)""")
        n = generate_random(num_digits)
        if miller_rabin(n, k):
            return n


# Parse the number of digits from the command line
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, required=True, help="# of digits")
args = parser.parse_args()
n = args.n
k = 10
confidence = 100 * (1 - 0.25 ** k)
n = generate_prime(n, k=k)
print(n)
print(f"is {ceil(log10(n))} digits prime with {confidence}% confidence")
