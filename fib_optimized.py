

# Dynamically -> Instantiate Cache information

def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


def f(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return f(n - 1) + f(n - 2)


def fib(n):
    if n < 0 and n % 2 == 0:
        return -f(abs(n))
    else:
        return f(n)


f = memoize(f)
result = fib(-1000)













