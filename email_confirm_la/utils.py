# coding: utf-8

import hashlib
import random


def generate_random_token(factors=None, hash_func=hashlib.sha256):
    if factors is None:
        factors = []

    bits = factors + [str(random.SystemRandom().getrandbits(512)), ]

    return hash_func(''.join(bits).encode('utf-8')).hexdigest()
