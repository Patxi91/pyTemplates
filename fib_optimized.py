import sys
sys.setrecursionlimit(50000)
import time

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
result = fib(-1000) # -43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875












# Dynamically -> Instantiate Cache information

cache = {}


def fib_dyn(n):

    # Base Case
    if n == 0 or n == 1:
        return n

    # Check cache
    if str(n) in cache:
        return cache[str(n)]
    else:  # Keep setting cache
        cache[str(n)] = fib_dyn(n - 1) + fib_dyn(n - 2)

    return cache[str(n)]


target = 300000 # nth Fibonacci

for n in range(0, target, 5000):
    fib_dyn(n)
    print(n)
    time.sleep(0.01)  # Seconds
result = fib_dyn(target)
