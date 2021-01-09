

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

    def insertLeft(self, newNode):
        # No Child --> insert
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        # Existing Child --> push it down the tree
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, value):
        self.key = value

    def getRootVal(self):
        return self.key


r = BinaryTree('a')
print(r.getRootVal())  # 'a'
print(r.getLeftChild())  # None
r.insertLeft('b')
print(r.getLeftChild().getRootVal())  # 'b'


# Tree Traversals: Preorder, inorder, postorder.

# Preorder: Root node -> recursive left preorder -> recursive right preorder
def preorder(tree):
    if tree:
        print(tree.getRootVal())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())


# Postorder: Recursive left postorder -> recursive right postorder -> root node
def postorder(tree):
    if tree != None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        print(tree.getRootVal())


# Inorder: Recursive left inorder -> root node -> Recursive right inorder
def inorder(tree):
    if tree != None:
        inorder(tree.getLeftChild())
        print(tree.getRootVal())
        inorder(tree.getRightChild())


# Priority Queues with Binary Heaps








