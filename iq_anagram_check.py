from nose.tools import assert_equals, assert_equal

# Interview question
'''
Anagram Check:
Given two strings, check to see if they are anagrams. An anagram is when the two strings can be written using the exact
same letters (so you can just rearrange the letters to get a different phrase or word).

For example:
"public relations" is an anagram of "crap built on lies."
"clint eastwood" is an anagram of "old west action"

Note: Ignore spaces and capitalization. So "d go" is an anagram of "God" and "dog" and "o d g".
'''


def anagram(s1, s2):
    s1_aux = s1.replace(" ", "").lower()
    s2_aux = s2.replace(" ", "").lower()
    return sorted(s1_aux) == sorted(s2_aux)


class AnagramTest(object):

    def test(self, sol):
        assert_equal(sol('go go go', 'gggooo'), True)
        assert_equal(sol('abc', 'cba'), True)
        assert_equal(sol('hi man', 'hi     man'), True)
        assert_equal(sol('aabbcc', 'aabbc'), False)
        assert_equal(sol('123', '1 2'), False)
        print("ALL TEST CASES PASSED")


# Run Tests
t = AnagramTest()
t.test(anagram)
