import argparse

from gmpy2 import mpz_random, random_state
from progress.bar import Bar, ShadyBar
from progress.spinner import LineSpinner, MoonSpinner, PieSpinner, \
    PixelSpinner, Spinner


def generate_prime(num_digits, k=10):
    # generate a random odd number with num_digits digits
    rs = random_state(42)

    def generate_random():
        min_n_digit_number = 10 ** (num_digits - 1)
        max_n_digit_number = 10 ** num_digits - 1
        delta = max_n_digit_number - min_n_digit_number
        while True:
            n = min_n_digit_number + mpz_random(rs, delta)
            if n % 10 in {1, 3, 7, 9}:
                return n

    # generate random numbers with num_digits digits until a prime is found.
    # Expected iterations is O(num_digits) due to the prime number theorem!
    expected = int(2.3 * num_digits)
    bar = ShadyBar('Generating primes ', max=num_digits, suffix='')
    for i in range(expected):
        n = generate_random()
        if n.is_probab_prime(k):
            print(' ')
            return n
        bar.next()
        if bar.index >= num_digits:
            bar.index *= 0.75


# Parse the number of digits from the command line
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, required=True, help="# of digits")
args = parser.parse_args()
n = args.n
k = 25
confidence = 100 * (1 - 0.25 ** k)
print(generate_prime(n, k=k))
print(f"is prime with {confidence}% confidence")
