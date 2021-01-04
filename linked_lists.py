# Singly Linked List Implementation.
'''
Pros: O(1) insertion/deletion vs Array's O(n).
Cons: O(k) access time from head to k-th element vs. Array's O(1).
'''


class Node:
    def __init__(self, value):
        self.value = value
        self.nextnode = None

a = Node(1)
b = Node(2)
c = Node(3)
a.nextnode = b
b.nextnode = c
print(a.value)  # 1
print(a.nextnode.value)  # 2


# Doubly Linked List Implementation.


class DoublyLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next_node = None
        self.prev_node = None


a = DoublyLinkedListNode(1)
b = DoublyLinkedListNode(2)
c = DoublyLinkedListNode(3)

a.next_node = b
b.prev_node = a

b.next_node = c
c.prev_node = b
