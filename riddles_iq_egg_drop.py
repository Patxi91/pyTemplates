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

arr = np.random.rand(100)  # generate 100 floors values
arr[np.random.randint(0, 100)] = 1  # Allocate limit floor represented with a value 1
print(f'The binary search did it in {binary_search(arr, 1)} drops this time!')  # n < (-1 + sqrt(1+8k))/2
