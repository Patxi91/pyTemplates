

# Tree representation through Lists
def BinaryTree(r):
    return [r, [], []]


def insertLeft(root, newBranch):
    t = root.pop(1)  # pop left tree

    if len(t) > 1:
        root.insert(1, [newBranch, t, []])
    else:
        root.insert(1, [newBranch, [], []])

    return root


def insertRight(root, newBranch):
    t = root.pop(2)  # pop left tree

    if len(t) > 1:
        root.insert(2, [newBranch, [], t])
    else:
        root.insert(2, [newBranch, [], []])

    return root


def getRootVal(root):
    return root[0]


def setRootVal(root, new_val):
    root[0] = new_val


def getLeftChild(root):
    return root[1]

def getRightChild(root):
    return root[2]


r = BinaryTree(3)
print(insertLeft(r, 4))  # [3, [4, [], []], []]
print(insertLeft(r, 5))  # [3, [5, [4, [], []], []], []]
print(insertRight(r, 6))  # [3, [5, [4, [], []], []], [6, [], []]]
print(insertRight(r, 7))  # [3, [5, [4, [], []], []], [7, [], [6, [], []]]]

l = getLeftChild(r)
print(l)  # [5, [4, [], []], []]
setRootVal(l, 9)
print(l)  # [9, [4, [], []], []]

print(r)  # [3, [9, [4, [], []], []], [7, [], [6, [], []]]]


# Nodes and References Implementation OOP
class BinaryTree:

    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None




