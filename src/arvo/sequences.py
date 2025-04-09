"""
Module for generating common integer sequences.

This module provides both precomputed constant sequences and functions that
generate sequences on-the-fly for common integer sequences, including:
  - A linear sequence (integers from 1 upward)
  - Prime numbers (via both a constant list and a generator)
  - Prime powers (precomputed)
  - Fibonacci numbers
  - Tribonacci numbers
  - Divisor counts for natural numbers (precomputed)
  - The Kolakoski sequence

The generative functions allow the user to specify a desired length, making the
module more flexible.
"""

import itertools

# Precomputed constant sequences

LINEAR = list(range(1, 200))

PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
    257,
    263,
    269,
    271,
]

PRIME_POWERS = [
    2,
    3,
    4,
    5,
    7,
    8,
    9,
    11,
    13,
    16,
    17,
    19,
    23,
    25,
    27,
    29,
    31,
    32,
    37,
    41,
    43,
    47,
    49,
    53,
    59,
    61,
    64,
    67,
    71,
    73,
    79,
    81,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    121,
    125,
    127,
    128,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    169,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
]

FIBONACCI = [
    1,
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    34,
    55,
    89,
    144,
    233,
    377,
    610,
    987,
    1597,
    2584,
    4181,
    6765,
    10946,
    17711,
    28657,
    46368,
    75025,
    121393,
    196418,
    317811,
    514229,
    832040,
    1346269,
    2178309,
    3524578,
    5702887,
    9227465,
    14930352,
    24157817,
    39088169,
    63245986,
    102334155,
]

TRIBONACCI = [
    1,
    1,
    2,
    4,
    7,
    13,
    24,
    44,
    81,
    149,
    274,
    504,
    927,
    1705,
    3136,
    5768,
    10609,
    19513,
    35890,
    66012,
    121415,
    223317,
    410744,
    755476,
    1389537,
    2555757,
    4700770,
    8646064,
    15902591,
    29249425,
    53798080,
    98950096,
    181997601,
    334745777,
    615693474,
    1132436852,
]

DIVISORS = [
    1,
    2,
    2,
    3,
    2,
    4,
    2,
    4,
    3,
    4,
    2,
    6,
    2,
    4,
    4,
    5,
    2,
    6,
    2,
    6,
    4,
    4,
    2,
    8,
    3,
    4,
    4,
    6,
    2,
    8,
    2,
    6,
    4,
    4,
    4,
    9,
    2,
    4,
    4,
    8,
    2,
    8,
    2,
    6,
    6,
    4,
    2,
    10,
    3,
    6,
    4,
    6,
    2,
    8,
    4,
    8,
    4,
    4,
    2,
    12,
    2,
    4,
    6,
    7,
    4,
    8,
    2,
    6,
    4,
    8,
    2,
    12,
    2,
    4,
    6,
    6,
    4,
    8,
    2,
    10,
    5,
    4,
    2,
    12,
    4,
    4,
    4,
    8,
    2,
    12,
    4,
    6,
    4,
    4,
    4,
    12,
    2,
    6,
    6,
    9,
    2,
    8,
    2,
    8,
]

# Generative functions for sequences


def linear(n: int) -> list[int]:
    """
    Generate a linear sequence of integers from 1 to n.

    Parameters:
        n (int): The length (upper bound) of the sequence.

    Returns:
        List[int]: A list of integers from 1 to n.
    """
    return list(range(1, n + 1))


def fibonacci(n: int) -> list[int]:
    """
    Generate the first n Fibonacci numbers.

    The Fibonacci sequence is defined by the recurrence relation:
        F(0) = 1, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1.

    Parameters:
        n (int): The number of Fibonacci numbers to generate.

    Returns:
        List[int]: A list containing the first n Fibonacci numbers.
    """
    if n <= 0:
        return []
    if n == 1:
        return [1]
    fib_seq = [1, 1]
    while len(fib_seq) < n:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq


def tribonacci(n: int) -> list[int]:
    """
    Generate the first n Tribonacci numbers.

    The Tribonacci sequence is defined by the recurrence relation:
        T(0) = 1, T(1) = 1, T(2) = 2, T(n) = T(n-1) + T(n-2) + T(n-3) for n > 2.

    Parameters:
        n (int): The number of Tribonacci numbers to generate.

    Returns:
        List[int]: A list containing the first n Tribonacci numbers.
    """
    if n <= 0:
        return []
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    trib_seq = [1, 1, 2]
    while len(trib_seq) < n:
        trib_seq.append(trib_seq[-1] + trib_seq[-2] + trib_seq[-3])
    return trib_seq


def primes(n: int) -> list[int]:
    """
    Generate the first n prime numbers using a simple trial division algorithm.

    Parameters:
        n (int): The number of prime numbers to generate.

    Returns:
        List[int]: A list containing the first n prime numbers.
    """
    if n <= 0:
        return []
    prime_numbers = []
    candidate = 2
    while len(prime_numbers) < n:
        is_prime = True
        for p in prime_numbers:
            if candidate % p == 0:
                is_prime = False
                break
            # No need to check beyond the square root of candidate
            if p * p > candidate:
                break
        if is_prime:
            prime_numbers.append(candidate)
        candidate += 1
    return prime_numbers


# Kolakoski sequence (credit to rosettacode.org)


def _cycler(start_items):
    """
    Create a cycling function that yields elements from start_items in cyclic order.

    Parameters:
        start_items (Iterable): A sequence of items to cycle.

    Returns:
        Function: A function that returns the next item in the cycle each time it is
        called.
    """
    return itertools.cycle(start_items).__next__


def _kolakoski_gen(start_items):
    """
    Internal generator for the Kolakoski sequence.

    Parameters:
        start_items (Tuple[int, ...]): The starting items of the Kolakoski sequence.

    Yields:
        int: The next number in the Kolakoski sequence.
    """
    s, k = [], 0
    c = _cycler(start_items)
    while True:
        c_next = c()
        s.append(c_next)
        sk = s[k]
        yield sk
        if sk > 1:
            s += [c_next] * (sk - 1)
        k += 1


def kolakoski(start_items=(1, 2), length=100) -> list[int]:
    """
    Generate a Kolakoski sequence of a specified length.

    The Kolakoski sequence is a self-generating sequence defined by a seed
    (default is (1, 2)) that then describes the sequence of its own run lengths.

    Parameters:
        start_items (Tuple[int, ...], optional): The starting items of the sequence.
        Defaults to (1, 2).
        length (int, optional): The desired length of the sequence. Defaults to 100.

    Returns:
        List[int]: A list containing the Kolakoski sequence of the specified length.
    """
    return list(itertools.islice(_kolakoski_gen(start_items), length))
