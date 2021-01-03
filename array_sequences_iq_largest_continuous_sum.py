from nose.tools import assert_equal

'''
Largest Continuous Sum:
Given an array of integers (positive and negative) find the largest continuous sum.
'''


def large_cont_sum(arr):

    if len(arr) == 0:
        return 0

    max_sum = current_sum = arr[0]

    for num in arr[1:]:
        current_sum = max(current_sum+num, num)
        max_sum = max(current_sum, max_sum)
    return max_sum


class TestPair:

    def test(self, sol):
        assert_equal(sol([1, 2, -1, 3, 4, 10, 10, -10, -1]), 29)
        print('ALL TEST CASES PASSED')


t = TestPair()
t.test(large_cont_sum)
