from nose.tools import assert_equal

'''
Array Pair Sum:
Given an integer array, output all the unique pairs that sum up to a specific value k.

So the input:
pair_sum([1,3,2,2],4)
would return 2 pairs:
 (1,3)
 (2,2)
NOTE: FOR TESTING PURPOSES CHANGE YOUR FUNCTION SO IT OUTPUTS THE NUMBER OF PAIRS
'''


def pair_sum(arr, k):

    if len(arr) < 2:
        return

    # Sets for tracking
    seen = set()
    output = set()

    for num in arr:
        target = k-num
        if target not in seen:
            seen.add(num)
        else:
            output.add( (min(num,target), max(num, target)) )

    return(len(output))


class TestPair:

    def test(self, sol):
        assert_equal(sol([1, 9, 2, 8, 3, 7, 4, 6, 5, 5, 13, 14, 11, 13, -1], 10), 6)
        assert_equal(sol([1, 2, 3, 1], 3), 1)
        assert_equal(sol([1, 3, 2, 2], 4), 2)
        print('ALL TEST CASES PASSED')


# Run tests
t = TestPair()
t.test(pair_sum)

'''
The O(N) algorithm uses the set data structure.
O(N) because we do a single linear scan of the array to check whether k-element is in the set of seen.
Insert and find operations of a set are both average O(1), so the algorithm is O(N) in total.
'''
