from nose.tools import assert_equal

'''
String Permutation:
Given a string, write a function that uses recursion to output a list of all the possible permutations of that string.
For example, given s='abc' the function should return ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
Note: If a character is repeated, treat each occurrence as distinct, so 'xxx' would return 6 "versions" of 'xxx'
'''


def permute(s):
    out = []

    # Base Case
    if len(s) == 1:
        out = [s]

    else:
        for i, let in enumerate(s):
            for perm in permute(s[:i] + s[i + 1:]):
                # Add it to output
                out += [let + perm]
    return out


class TestPerm(object):

    def test(self, solution):
        assert_equal(sorted(solution('abc')), sorted(['abc', 'acb', 'bac', 'bca', 'cab', 'cba']))
        assert_equal(sorted(solution('dog')), sorted(['dog', 'dgo', 'odg', 'ogd', 'gdo', 'god']))
        print('PASSED ALL TEST CASES!')


# Run Tests
t = TestPerm()
t.test(permute)
