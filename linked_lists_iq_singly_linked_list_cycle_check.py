from nose.tools import assert_equal

'''
Singly Linked List Cycle Check:

Write a function which takes in the first node in a singly linked list and returns a boolean indicating if the linked list contains a "cycle".
A cycle is when a node's next point actually points back to a previous node in the list.
This is also sometimes known as a circularly linked list.
Given the Linked List Node class:
class Node:

    def __init__(self, value):
        self.value = value
        self.nextnode = None
'''


class Node:

    def __init__(self, value):
        self.value = value
        self.nextnode = None


def cycle_check(node):

    marker1 = node
    marker2 = node

    while marker2 != None and marker2.nextnode != None:
        marker1 = marker1.nextnode
        marker2 = marker2.nextnode.nextnode
        if marker2 == marker1:
            return True
    return False


# CREATE CYCLE LIST
a = Node(1)
b = Node(2)
c = Node(3)

a.nextnode = b
b.nextnode = c
c.nextnode = a  # Cycle Here!

# CREATE NON CYCLE LIST
x = Node(1)
y = Node(2)
z = Node(3)

x.nextnode = y
y.nextnode = z


#############
class TestCycleCheck(object):

    def test(self, sol):
        assert_equal(sol(a), True)
        assert_equal(sol(x), False)

        print("ALL TEST CASES PASSED")


# Run Tests

t = TestCycleCheck()
t.test(cycle_check)
