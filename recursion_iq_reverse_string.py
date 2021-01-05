from nose.tools import assert_equal

'''
Reverse a String:
Reverse a string using recursion.
Do not slice (e.g. string[::-1]) or use iteration, there must be a recursive call for the function.
'''


def reverse1(s):
    if len(s) <= 1:
        return s
    else:
        m = int(len(s)/2)
        return reverse1(s[m:]) + (reverse1((s[:m])))


def reverse2(s):
    if s != '':
        return s[-1]+reverse2(s[:-1])
    else:
        return s


def reverse3(s):
    if len(s) <= 1:
        return s
    else:
        return reverse3(s[1:]) + s[0]





class TestReverse(object):

    def test_rev(self, solution):
        assert_equal(solution('e'), 'e')
        assert_equal(solution('hello'), 'olleh')
        assert_equal(solution('hello world'), 'dlrow olleh')
        assert_equal(solution('123456789'), '987654321')

        print('PASSED ALL TEST CASES!')


# Run Tests
test = TestReverse()
test.test_rev(reverse1)
test.test_rev(reverse2)
test.test_rev(reverse3)
