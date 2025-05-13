import argparse
import random
from math import ceil, log10
from time import time

import numpy as np
from gmpy2 import powmod


class App:
    def __init__(self, digits, iterations, seed=42):
        self.digits = digits
        self.iterations = iterations
        self.seed = seed
        random.seed(seed)
        self.small_primes = self._get_small_primes()

    @staticmethod
    def _get_small_primes():
        # first 100 primes
        small_primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
            61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131,
            137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
            199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
            277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
            359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,
            439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509,
            521, 523, 541
        ]
        return small_primes

    def is_divisible_by_small_prime(self, n):
        """
        condition 1 (Fermat's Little Theorem)
        """
        return any(n % p == 0 for p in self.small_primes)

    def miller_rabin_iteration(self, n):
        # First, see if n is divisible by one of the first 100 primes
        # Sometimes this will shortcut, and we immediately find n is composite
        if self.is_divisible_by_small_prime(n) and n > self.small_primes[-1]:
            return False

        a = self._pick_random_base(n)
        e = self._start_expoent(n)
        if self._fermat_little_theorem(a, e, n):
            return False

        prev_is1 = True
        while self._is_even(e):
            e //= 2
            x = powmod(a, e, n)
            if prev_is1:  # condition 2
                if x == n - 1:
                    prev_is1 = False
                elif x != 1:
                    return False
        return True

    @staticmethod
    def _is_even(e):
        return not e & 1 # 1000: 3.0629 (35) s | 2000: 24,4839 (84) s
        # return e % 2 == 0  # 1000: 3.0622 (38) s | 2000: 24,4940 (65) s

    @staticmethod
    def _start_expoent(n):
        return n - 1

    @staticmethod
    def _pick_random_base(n):
        return random.randint(2, n - 1)

    @staticmethod
    def _fermat_little_theorem(a, e, n):
        return powmod(a, e, n) != 1

    def miller_rabin(self, n):
        # Iterate the Miller-Rabin test k times
        # achieves >= (1 - 0.25^k) confidence
        for _ in range(self.iterations):
            if not self.miller_rabin_iteration(n):
                return False
        return True

    def generate_random(self):
        min_n_digit_number = 10 ** (self.digits - 2)
        max_n_digit_number = 10 ** (self.digits - 1) - 1
        last_digit = random.choice([1, 3, 7, 9])
        n = random.randint(min_n_digit_number, max_n_digit_number)
        return n * 10 + last_digit

    def generate_prime(self):
        # generate random numbers with num_digits digits until a prime is found.
        # Expected iterations is O(num_digits) due to the prime number theorem!
        expected = int(2.3 * self.digits)
        for i in range(1, expected):
            print(
                f"""iteration: {i} (expected <= {expected} total due to PNT)""")
            n = self.generate_random()
            if self.miller_rabin(n):
                return n

    def run(self):
        confidence = 100 * (1 - 0.25 ** self.iterations)
        n = self.generate_prime()
        print(n)
        print(f"is {ceil(log10(n))} digits prime "
              f"with {confidence}% confidence")


def _get_argparser():
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

def _measure_times():
    times = np.array([])
    for i in range(10):
        app = App(2000, 10, 42)
        print(f'Measuring {i+1}/10...')
        start_time = time()
        app.generate_prime()
        elapsed_time = time() - start_time
        times = np.append(times, elapsed_time)
    _report_times_result(times)

def _report_times_result(times):
    mean = np.mean(times)
    std = np.std(times)
    stdmean = std / np.sqrt(len(times))

    print(f"mean: {mean:.4f} s")
    print(f"stdmean: {stdmean:.4f} s")

def _invoke_app(digits, iterations, seed):
    app = App(digits, iterations, seed)
    app.run()

def main():
    parser = _get_argparser()
    args = parser.parse_args()
    n = args.digits
    k = args.iterations
    seed = args.seed
    _invoke_app(n, k, seed)
    # _measure_times()

if __name__ == "__main__":
    main()
