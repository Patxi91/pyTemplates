
'''
Write a function to reverse a Linked List in place.
The function will take in the head of the list as input and return the new head of the list.
You are given the example Linked List Node class:
class Node:
    def __init__(self,value):

        self.value = value
        self.nextnode = None
'''

# O(1)-O(n) space-time solution.

class Node:
    def __init__(self, value):

        self.value = value
        self.nextnode = None


def reverse(head):
    # Set up current,previous, and next nodes
    current = head
    previous = None
    nextnode = None

    # until we have gone through to the end of the list
    while current:
        # Make sure to copy the current nodes next node to a variable next_node
        # Before overwriting as the previous node for reversal
        nextnode = current.nextnode

        # Reverse the pointer ot the next_node
        current.nextnode = previous

        # Go one forward in the list
        previous = current
        current = nextnode

    return previous

# Create a list of 4 nodes
a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
# Set up order a,b,c,d with values 1,2,3,4
a.nextnode = b
b.nextnode = c
c.nextnode = d

print(a.nextnode.value)  # 2
print(b.nextnode.value)  # 3
print(c.nextnode.value)  # 4
#print(d.nextnode.value)  # This will give an error since it points to None

# Run Test
reverse(a)

print(d.nextnode.value)  # 3
print(c.nextnode.value)  # 2
print(b.nextnode.value)  # 1
#print(a.nextnode.value)  # This will give an error since it now points to None
