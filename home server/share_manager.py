import random

P = 2**127 - 1  # Large prime

def split_secret(hex_key, t=2, n=3):
    secret = int(hex_key, 16)
    coeffs = [secret] + [random.randint(0, P - 1) for _ in range(t - 1)]

    def f(x):
        return sum(c * (x ** i) for i, c in enumerate(coeffs)) % P

    return [(x, f(x)) for x in range(1, n + 1)]
