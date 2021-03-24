# Dynamically -> Instantiate Cache information --> Execution Timed Out (12000 ms)

cache = {}


def fib_dyn(n):
    # Base Case
    if n == 0 or n == 1:
        return n

    # Check cache
    if n in cache:
        return cache[n]
    else:  # Keep setting cache
        cache[n] = fib_dyn(n - 1) + fib_dyn(n - 2)

    return cache[n]


def fib_cache(target):
    step = 900
    if target < 0 and target % 2 == 0:
        for n in range(0, abs(target), step):
            fib_dyn(n)
        return -fib_dyn(abs(target))
    elif target < 0:
        for n in range(0, abs(target), step):
            fib_dyn(n)
        return fib_dyn(abs(target))
    else:
        for n in range(0, target, step):
            fib_dyn(n)
        return fib_dyn(target)


# Mathematical Approach

def fib(n):
    if n >= 0:
        return fibiter(1, 0, 0, 1, n)
    if n < 0:
        a, b = 0, 1
        for _ in range(0, n, -1):
            a, b = b - a, a
        return a


def fibiter(a, b, p, q, count):
    if count == 0:
        return b
    if count % 2 == 0:
        return fibiter(a, b, p * p + q * q, q * q + 2 * p * q, count / 2)
    else:
        return fibiter(b * q + a * q + a * p, b * p + a * q, p, q, count - 1)
