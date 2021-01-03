from nose.tools import assert_equal

'''
Sentence Reversal:
Given a string of words, reverse all the words.
Given:
'This is the best'
Return:
'best the is This'
Note: You should remove all leading and trailing whitespace. So that inputs such as:
'  space here'  and 'space here      '
both become:
'here space'
'''


def rev_word1(s):
    aux = ''
    arr = []
    for i in range(0, len(s)):
        if s[i] != ' ':
            aux += s[i]
        else:
            if aux != '':
                arr.append(aux)
                aux = ''
            pass
    if aux != '':
        arr.append(aux)
    aux = arr[-1]
    for word in arr[-2::-1]:
        aux += ' ' + word
    return aux


def rev_word2(s):

    words = []
    length = len(s)
    space = [' ']
    i = 0

    while i < length:
        if s[i] not in space:
            word_start = i
            while i < length and s[i] not in space:
                i += 1
            words.append(s[word_start:i])
        i += 1
    return ' '.join(reversed(words))


def rev_word3(s):
    return " ".join(reversed(s.split()))


def rev_word4(s):
    return " ".join(s.split()[::-1])


class Test:

    def test(self, sol):
        assert_equal(sol('    space before'), 'before space')
        assert_equal(sol('space after     '), 'after space')
        assert_equal(sol('   Hello John    how are you   '), 'you are how John Hello')
        assert_equal(sol('1'), '1')
        print('ALL TEST CASES PASSED')


# Run and test
t = Test()
t.test(rev_word1)
t.test(rev_word2)
t.test(rev_word3)
t.test(rev_word4)
