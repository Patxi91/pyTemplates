from enum import Enum
from collections import OrderedDict

'''
The graph is directed and the edges can hold weights.
Three classes: a State class, a Node class, and the Graph class.
Uses:
Enum --> Support for enumerations in the State class, see https://docs.python.org/3/library/enum.html
OrderDict --> Dictionary + remembers the order in which the keys were inserted in, see https://docs.python.org/3/library/collections.html#collections.OrderedDict
'''


class State(Enum):
    unvisited = 1
    visited = 2
    visiting = 3


class Node:

    def __init__(self, num):
        self.num = num
        self.visit_state = State.unvisited
        self.adjacent = OrderedDict()  # key = node, value = weight

    def __str__(self):
        return str(self.num)


class Graph:

    def __init__(self):
        self.nodes = OrderedDict()

    def add_node(self, num):
        node = Node(num)
        self.nodes[num] = node
        return node

    def add_edge(self, fn, tn, weight=0):  # from node --> to node
        if fn not in self.nodes:
            self.add_node(fn)
        if tn not in self.nodes:
            self.add_node(tn)
        self.nodes[fn].adjacent[self.nodes[tn]] = weight  # adjacent is OrderedDict of Node


g = Graph()
g.add_edge(0, 1, 5)
print(g.nodes)  # OrderedDict([(0, <__main__.Node object at 0x04493958>), (1, <__main__.Node object at 0x0454F3E8>)])
g.add_edge(1, 2, 3)
print(g.nodes)  # OrderedDict([(0, <__main__.Node object at 0x03C90430>), (1, <__main__.Node object at 0x03C90358>), (2, <__main__.Node object at 0x03C90220>)])
