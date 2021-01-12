from nose.tools import assert_equal

"""
Binary Search Tree Check:
Given a binary tree, check whether it’s a binary search tree or not.
Hint: Think about tree traversals.
"""


class Node:

    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.left = left
        self.right = right
        self.parent = parent


# Keep track of min and max values a Node can take as we go through the Tree.
def tree_max(node):
    if not node:
        return float("-inf")
    maxleft = tree_max(node.left)
    maxright = tree_max(node.right)
    return max(node.key, maxleft, maxright)


def tree_min(node):
    if not node:
        return float("inf")
    minleft = tree_min(node.left)
    minright = tree_min(node.right)
    return min(node.key, minleft, minright)


def verify(node):
    if not node:
        return True
    if (tree_max(node.left) <= node.key <= tree_min(node.right) and
        verify(node.left) and verify(node.right)):
        return True
    else:
        return False


# In a BST, traversing the Tree in order should lead to a sorted order of Nodes
def inorder(tree, tree_vals=None):
    if tree != None:
        inorder(tree.left, tree_vals)
        tree_vals.append(tree.key)
        inorder(tree.right, tree_vals)
    return tree_vals


def sort_check(root):
    tree_vals = inorder(root, [])
    return tree_vals == sorted(tree_vals)


class TestCoins(object):

    def check(self):

        root= Node(10, "Hello")
        root.left = Node(5, "Five")
        root.right= Node(30, "Thirty")

        # True, since this tree is valid
        assert_equal(verify(root), True)
        assert_equal(sort_check(root), True)

        root = Node(10, "Ten")
        root.right = Node(20, "Twenty")
        root.left = Node(5, "Five")
        root.left.right = Node(15, "Fifteen")

        # False, since 15 is to the left of 10
        assert_equal(verify(root), False)
        assert_equal(sort_check(root), False)

        print('PASSED ALL TEST CASES!')


# Run Test

test = TestCoins()
test.check()
