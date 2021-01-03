from nose.tools import assert_equal
import collections

'''
Find the Missing Element:
Consider an array of non-negative integers.
A second array is formed by shuffling the elements of the first array and deleting a random element.
Given these two arrays, find which element is missing in the second array.

Here is an example input, the first array is shuffled and the number 5 is removed to construct the second array.
Input:
finder([1,2,3,4,5,6,7],[3,7,2,1,4,6])
Output:
5 is the missing number
'''


def finder(arr1, arr2):

    # Sort the arrays
    arr1.sort()
    arr2.sort()

    for num1, num2 in zip(arr1, arr2):
        if num1 != num2:
            return num1
    return arr1[-1]


def finder2(arr1, arr2):

    # Using default dict to avoid key errors
    d=collections.defaultdict(int)

    for num in arr2:
        d[num] += 1
    # Check if num not in dictionary
    for num in arr1:
        if d[num] == 0:
            return num
        else:
            d[num] -= 1


# O(N) time and O(1) space complexity


def finder3(arr1, arr2):
    result = 0

    # Perform an XOR between the numbers in the arrays
    for num in arr1 + arr2:
        result ^= num
        print(result)

    return result


class TestPair:

    def test(self, sol):
        assert_equal(sol([1,2,3,4,5,6,7],[3,7,2,1,4,6]), 5)
        assert_equal(sol([5, 5, 7, 7], [5, 7, 7]), 5)
        print('ALL TEST CASES PASSED')


# Run tests
t = TestPair()
t.test(finder)
t.test(finder2)
t.test(finder3)
