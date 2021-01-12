
'''
Trim a Binary Search Tree:
Given the root of a BST and a min and max, trim the tree such that all the numbers are between min and max (inclusive).
The resulting tree should still be a valid binary search tree.
'''

class Node:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

def inorder(tree):
    if tree != None:
        inorder(tree.left)
        print(tree.val)
        inorder(tree.right)

def trimBST(tree, minVal, maxVal):
    if not tree:
        return

    tree.left = trimBST(tree.left, minVal, maxVal)
    tree.right = trimBST(tree.right, minVal, maxVal)

    if minVal <= tree.val <= maxVal:
        return tree

    if tree.val < minVal:
        return tree.right

    if tree.val > maxVal:
        return tree.left


# Run Tests

root = Node(1)
root.right = Node(3)
root.left = Node(2)
root.left.left = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)

trimbst = trimBST(root, 2, 5)
inorder(trimbst)
