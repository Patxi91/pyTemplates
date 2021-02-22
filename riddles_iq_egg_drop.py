import math
import numpy as np

'''
Egg Drop:

A tower has 100 floors. There are two eggs to test.
The eggs are strong enough that they can be dropped from a particular floor in the tower without breaking.
The goal is to find the highest floor an egg can be dropped without breaking, in as few drops as possible.
If an egg is dropped from above its target floor it will break.
If it is dropped from that floor or below, it will be intact and you can test drop the egg again on another floor.

How to go about doing this in as few drops as possible?: Fewest drops needed for testing 2 eggs on 100 floors.


Approach:

Input : k = 10
Output : 4
We first try from 4-th floor. Two cases arise,
(1) If egg breaks, we have one egg left so we
    need three more trials.
(2) If egg does not break, we try next from 7-th
    floor. Again two cases arise.
We can notice that if we choose 4th floor as first
floor, 7-th as next floor and 9 as next of next floor,
we never exceed more than 4 trials.

Input : k = 100
Output : 14

If first egg has not broken so far, then the i-th trial has to be from floor number x + (x – 1) + … + (x – i – 1).
So we can cover x + (x – 1) + (x – 2) …. + 2 + 1 floors with x trials. The value of this expression is x * (x + 1) / 2.
Then the optimal x for a given k floors is: x * (x + 1)/2 >= k  --> if k=100 then x=13.65 that is 14.
The optimal value of x can be written as: (-1 + sqrt(1+8k))/2

If n =100, then x would be 13.65 which since we can't drop from a decimal of a floor, we actually use 14.
So, the worst case scenario is now when the threshold is in the first 14 floors with number of drops being 14.
'''


# Optimal number of trials for k floors and 2 eggs
def twoEggDrop(k):
    return math.ceil((-1 + math.sqrt(1 + 8*k)) / 2)


# Binary Search O(log2 (n))
def binary_search(arr, ele):
    drops = 0

    first = 0
    last = len(arr)-1
    found = False

    while first <= last and not found:
        mid = (first+last) // 2
        if arr[mid] == ele:
            drops += 1
            found = True
        else:
            if ele < arr[mid]:
                drops += 1
                last = mid-1  # use lower half
            else:
                drops += 1
                first = mid+1  # use upper half
    return drops if found else None


# Driver
k = 100
print(f'The worst scenario with 2 eggs and 100 floors would be {twoEggDrop(k)} drops.')

arr = np.arange(1, 101, 1)  # generate 100 floors values
highest_floor = 79  # highest floor the egg could be thrown without breaking
print(f'The binary search found floor #{highest_floor} in {binary_search(arr, highest_floor)} drops!')  # The binary search found floor #79 in 6 drops!, n < (-1 + sqrt(1+8k))/2

