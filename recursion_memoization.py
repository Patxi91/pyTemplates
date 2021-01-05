# Factorials using memoization

factorial_memo = {}  # Dictionary creates cache for known results


def factorial(k):
    if k < 2:
        return 1

    if k not in factorial_memo:
        factorial_memo[k] = k * factorial(k - 1)

    return factorial_memo[k]


print(factorial(4))  # 24


# Encapsulate the memoization process into a class
class Memoize:

    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


def factorial_class(k):
    if k < 2:
        return 1

    return k * factorial_class(k - 1)


f = Memoize(factorial_class)
print(f(4))  # 24
