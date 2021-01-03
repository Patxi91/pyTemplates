from nose.tools import assert_equal

'''
Balanced Parentheses Check:
Given a string of opening and closing parentheses, check whether it’s balanced. We have 3 types of parentheses: round brackets: (), square brackets: [], and curly brackets: {}. Assume that the string doesn’t contain any other character than these, no spaces words or numbers. As a reminder, balanced parentheses require every opening parenthesis to be closed in the reverse order opened. For example ‘([])’ is balanced but ‘([)]’ is not.
You can assume the input string has no spaces.
'''


# Stack
def balance_check1(s):
    chars = []
    matches = {')':'(',']':'[','}':'{'}
    for c in s:
        if c in matches:
            if chars.pop() != matches[c]:
                return False
        else:
            chars.append(c)
    return chars == []


# Stack
def balance_check2(s):
    # Check is even number of brackets
    if len(s) % 2 != 0:
        return False

    # Set of opening brackets
    opening = set('([{')

    # Matching Pairs
    matches = set([('(', ')'), ('[', ']'), ('{', '}')])

    # Use a list as a "Stack"
    stack = []

    # Check every parenthesis in string
    for paren in s:

        # If its an opening, append it to list
        if paren in opening:
            stack.append(paren)

        else:

            # Check that there are parentheses in Stack
            if len(stack) == 0:
                return False

            # Check the last open parenthesis
            last_open = stack.pop()

            # Check if it has a closing match
            if (last_open, paren) not in matches:
                return False

    return len(stack) == 0


# Counter to Zero
def balance_check3(s):
    round_b = square_b = curly_b = 0
    list_s = list(s)
    while list_s:
        char = list_s.pop(-1)

        if char == '(':
            round_b += 1
        elif char == ')':
            round_b -= 1
        elif char == '[':
            square_b += 1
        elif char == ']':
            square_b -= 1
        elif char == '{':
            curly_b += 1
        else:
            curly_b -= 1

    return True if round_b == 0 and square_b == 0 and curly_b == 0 else False


class TestBalanceCheck:

    def test(self, sol):
        assert_equal(sol('[](){([[[]]])}('), False)
        assert_equal(sol('[{{{(())}}}]((()))'), True)
        assert_equal(sol('[[[]])]'), False)
        print('ALL TEST CASES PASSED')


# Run Tests
t = TestBalanceCheck()
t.test(balance_check1)
t.test(balance_check2)
t.test(balance_check3)
