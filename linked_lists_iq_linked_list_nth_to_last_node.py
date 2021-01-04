from nose.tools import assert_equal

'''
Linked List Nth to Last Node:
Write a function that takes a head node and an integer value n and then returns the nth to last node in the linked list.
Given:
class Node:

    def __init__(self, value):
        self.value = value
        self.nextnode  = None
'''


class Node:

    def __init__(self, value):
        self.value = value
        self.nextnode = None


def nth_to_last_node(n, head):
    left_pointer = head
    right_pointer = head

    # Set right pointer at n nodes away from head
    for i in range(n - 1):

        # Check for edge case of not having enough nodes!
        if not right_pointer.nextnode:
            raise LookupError('Error: n is larger than the linked list.')

        # Otherwise, we can set the block
        right_pointer = right_pointer.nextnode

    # Move the block down the linked list
    while right_pointer.nextnode:
        left_pointer = left_pointer.nextnode
        right_pointer = right_pointer.nextnode

    # Now return left pointer, its at the nth to last element!
    return left_pointer


a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
e = Node(5)

a.nextnode = b
b.nextnode = c
c.nextnode = d
d.nextnode = e


####

class TestNLast(object):

    def test(self, sol):
        assert_equal(sol(2, a), d)  # This would return the node d with a value of 4, because its the 2nd to last node.
        print('ALL TEST CASES PASSED')


# Run tests
t = TestNLast()
t.test(nth_to_last_node)
