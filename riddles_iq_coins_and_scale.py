import math

'''
Coins and a Scale:

Having eight coins and a two-pan scale. All the coins weigh the same, except one which is heavier than all the others.
The coins are otherwise indistinguishable. There are no assumptions about how much heavier the heavy coin is.
What is the minimum number of weightings needed to be certain of identifying the heavy coin?

coins array = [1, 1, 1, 1, 1, 1, 2, 1]
'''


# O(log n)
def find_heavy_coin(coins):

    if len(coins) == 1:
        print(f'Heavy coin weights {coins[0]}')
        return coins[0]

    group_size = math.ceil(len(coins)/3)
    A = coins[:group_size]
    sumA = sum(A)
    B = coins[group_size:2*group_size]
    sumB = sum(B)
    C = coins[2*group_size:]

    if sumA != sumB:
        if sumA > sumB:
            find_heavy_coin(A)
        else:
            find_heavy_coin(B)
    else:
        find_heavy_coin(C)


coins = [1, 1, 1, 1, 1, 1, 2, 1]
find_heavy_coin(coins)  # Heavy coin weights 2
