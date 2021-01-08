from nose.tools import assert_equal

"""
Coin Change Problem:
Given a target amount n and a list (array) of distinct coin values, what's the fewest coins needed to make the change amount.

For example:
If n = 10 and coins = [1,5,10]. Then there are 4 possible ways to make change:

1+1+1+1+1+1+1+1+1+1
5 + 1+1+1+1+1
5+5
10

With 1 coin being the minimum amount.
"""


# Recursive - slow
def rec_coin(target, coins):

    min_coins = target

    if target in coins:
        return 1
    else:

        for i in [c for c in coins if c <= target]:
            num_coins = 1 + rec_coin(target-i, coins)

            if num_coins < min_coins:
                min_coins = num_coins

    return min_coins


# Recursive caching - fast
def rec_coin_cache(target, coins, known_results):

    # Default output to target
    min_coins = target

    # Base Case
    if target in coins:
        known_results[target] = 1
        return 1

    # Return a known result if it happens to be greater than 1
    elif target in known_results:
        return known_results[target]

    else:
        # for every coin value that is <= than target
        for i in [c for c in coins if c <= target]:

            # Recursive call
            num_coins = 1 + rec_coin_cache(target-i, coins, known_results)

            # Reset Minimum if we have a new minimum
            if num_coins < min_coins:
                min_coins = num_coins

                # Reset the known result
                known_results[target] = min_coins

    return min_coins


# Dynamically
def rec_coin_dyn(change, coinValueList, minCoins):

    for cents in range(change+1):
        coinCount = cents
        for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
                coinCount = minCoins[cents-j]+1
        minCoins[cents] = coinCount

    return minCoins[change]


class TestCoins(object):

    def check(self,solution):
        coins = [1,5,10,25]
        if solution == rec_coin:
            assert_equal(solution(45,coins),3)
            assert_equal(solution(23,coins),5)
            assert_equal(solution(74,coins),8)
            print('PASSED ALL TEST CASES!')
        elif solution == rec_coin_cache or solution == rec_coin_dyn:
            known_results = {}
            target = 45
            assert_equal(solution(target,coins,known_results),3)
            target = 23
            assert_equal(solution(target,coins,known_results),5)
            target = 74
            assert_equal(solution(target,coins,known_results),8)
            print('PASSED ALL TEST CASES!')


# Run Test

test = TestCoins()
test.check(rec_coin_cache)
test.check(rec_coin_dyn)
