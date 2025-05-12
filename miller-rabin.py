import argparse

from gmpy2 import mpz_random, random_state
from progress.bar import ShadyBar


class App:
    def __init__(self, num_digits, miller_rabin_iterations=10):
        self.rs = random_state(42)
        self.num_digits = num_digits
        self.miller_rabin_iterations = miller_rabin_iterations

    def generate_random(self):
        min_n_digit_number = 10 ** (self.num_digits - 1)
        max_n_digit_number = 10 ** self.num_digits - 1
        delta = max_n_digit_number - min_n_digit_number
        while True:
            n = min_n_digit_number + mpz_random(self.rs, delta)
            if n % 10 in {1, 3, 7, 9}:
                return n

    def generate_prime(self):
        # generate random numbers with num_digits digits until a prime is found.
        # Expected iterations is O(num_digits) due to the prime number theorem!
        expected = int(2.3 * self.num_digits)
        bar = ShadyBar('Generating primes ',
                       max=self.num_digits,
                       suffix='')
        for i in range(expected):
            n = self.generate_random()
            if n.is_probab_prime(self.miller_rabin_iterations):
                print(' ')
                return n
            bar.next()
            if bar.index >= self.num_digits:
                bar.index *= 0.75

    def run(self):
        confidence = 100 * (1 - 0.25 ** self.miller_rabin_iterations)
        print(self.generate_prime())
        print(f"is prime with {confidence}% confidence")


def main():
    # Parse the number of digits from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, required=True, help="# of digits")
    args = parser.parse_args()
    n = args.n
    app = App(n, 10)
    app.run()


if __name__ == '__main__':
    main()
