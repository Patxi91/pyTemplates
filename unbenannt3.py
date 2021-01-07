from nose.tools import assert_equal
import time


# Dynamic solution Coins
def coin_dyn(n, coins):
    
    min_c = n
    
    if n in coins:
        return 1
    
    elif n in cache:
        return cache[n]
    
    else:
        for i in [c for c in coins if c <= n]:
            cache[i] = 1 + coin_dyn(n-i, coins)
            print(n,i,cache)
            if cache[i] < min_c:
                min_c = cache[i]
                print('here')
    
    return cache[n]


cache = {}
n = 74
coins = [1, 5, 10, 25]
print(coin_dyn(n, coins))  # 8

















