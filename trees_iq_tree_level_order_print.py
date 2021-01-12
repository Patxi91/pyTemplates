import operator
import collections

"""
Tree Level Order Print:
Given a binary tree of integers, print it in level order.
The output will contain space between the numbers in the same level, and new line between different levels.
For example:

root = Node(1)
root.right = Node(3)
root.left = Node(2)
root.left.left = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)

The output should be:

1 
2 3 
4 5 6
"""


class Node:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

# Traverse and map keys to levels
def inorder(tree, level, tree_vals=None):
    if tree != None:
        inorder(tree.left, level+1, tree_vals)
        tree_vals[str(tree.val)] = level
        inorder(tree.right, level+1, tree_vals)
    return tree_vals


def levelOrderPrint1(tree):
    tree_vals = inorder(tree, 0, {})  # Start in root == level 0
    order = []
    tmp = []
    for i in range(tree_vals[max(tree_vals.items(), key=operator.itemgetter(1))[0]] + 1):
        for j in tree_vals:
            if tree_vals[j] == i:
                tmp.append(int(j))
        order.append(tmp)
        tmp = []
    for ele in order:
        print(*ele, sep=' ')
    pass


# Using a deque and counters for nodes in each level:
# Current level count indicates how many nodes should be printed at this level before printing a new line.
def levelOrderPrint2(tree):
    if not tree:
        return
    nodes=collections.deque([tree])
    currentCount, nextCount = 1, 0
    while len(nodes)!=0:
        currentNode=nodes.popleft()
        currentCount-=1
        print(currentNode.val, end=' ')
        if currentNode.left:
            nodes.append(currentNode.left)
            nextCount+=1
        if currentNode.right:
            nodes.append(currentNode.right)
            nextCount+=1
        if currentCount==0:
            #finished printing current level
            print('\n')
            currentCount, nextCount = nextCount, currentCount



# Run Tests

root = Node(1)
root.right = Node(3)
root.left = Node(2)
root.left.left = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)

levelOrderPrint1(root)
levelOrderPrint2(root)

'''
output:
1
2 3
4 5 6
'''
