import argparse
from random import choice

from gmpy2 import mpz_random, random_state
from progress.bar import ShadyBar


class App:
    def __init__(self, num_digits, miller_rabin_iterations=10, seed=42):
        self.rs = random_state(seed)
        self.num_digits = num_digits
        self.miller_rabin_iterations = miller_rabin_iterations

    def generate_random(self):
        lower_num = 10 ** (self.num_digits - 2)
        upper_num = 10 ** (self.num_digits - 1) - 1
        delta = upper_num - lower_num
        last_digit = choice([1, 3, 7, 9])
        n = lower_num + mpz_random(self.rs, delta)
        return n * 10 + last_digit

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
        prime = self.generate_prime()
        print(prime)
        print(f"is prime with {confidence}% confidence")
        print(f'{len(prime.digits())} digits')


def main():
    parser = _get_parser()
    args = parser.parse_args()
    n = args.digits
    seed = args.seed
    k = args.iterations
    app = App(n, k, seed)
    app.run()


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--digits',
                        type=int,
                        required=True,
                        help="# of digits")
    parser.add_argument('-i', '--iterations',
                        type=int,
                        required=False,
                        default=10,
                        help="# of Miller-Rabin iterations")
    parser.add_argument('-s', '--seed',
                        type=int,
                        required=False,
                        default=42,
                        help="seed for random number generation")
    return parser


if __name__ == '__main__':
    main()
