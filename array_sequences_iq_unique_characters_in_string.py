from nose.tools import assert_equal

# Interview question
'''
Unique Characters in String:
Given a string,determine if it is compressed of all unique characters. 
The string 'abcde' has all unique characters and should return True.
The string 'aabcde' contains duplicate characters and should return False.
'''


def uni_char1(s):
    return len(set(s)) == len(s)


def uni_char2(s):
    chars = set()

    for let in s:
        # Check if in set
        if let in chars:
            return False
        else:
            chars.add(let)
    return True


class Test:

    def test(self, sol):
        assert_equal(sol(''), True)
        assert_equal(sol('goo'), False)
        assert_equal(sol('abcdefg'), True)
        print('ALL TEST CASES PASSED')


# Run and test
t = Test()
t.test(uni_char1)
t.test(uni_char2)
