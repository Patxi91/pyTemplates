from nose.tools import assert_equal

# Interview question
'''
Largest Continuous Sum:
Given an array of integers (positive and negative) find the largest continuous sum.
'''


def large_cont_sum(k):
    return k


class TestPair:

    def test(self, sol):
        assert_equal(sol(5), 5)
        print('ALL TEST CASES PASSED')


t = TestPair()
t.test(large_cont_sum)


