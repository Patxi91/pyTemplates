'''
Implement a Stack:

It should have the methods:
Check if its empty
Push a new item
Pop an item
Peek at the top item
Return the size
'''


# Implementation of a Stack (1 end: top)
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


print('Stack')
s = Stack()
print(s.isEmpty())  # True
s.push(1)
s.push('Two')
print(s.peek())  # 'Two'
s.push(True)
print(s.size())  # 3
print(s.isEmpty())  # False
print(s.pop())  # True
print(s.pop())  # 'Two'
print(s.pop())  # 1
print(s.isEmpty())  # True


'''
Implement a Queue:

It should have the methods:
Check if Queue is Empty
Enqueue
Dequeue
Return the size of the Queue
'''


# Implementation of a Queue (2 ends: rear, front)
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


print('Queue')
q = Queue()
print(q.isEmpty())  # True
q.enqueue(1)
q.enqueue(2)
print(q.dequeue())  # 1 (1st in 1st out)


'''
Implement a Deque:

It should have the methods:
Check if its empty
Add to both front and rear
Remove from Front and Rear
Check the Size
'''


# Implementation of a Deque (aka. double-ended queue w/ 2 ends: rear, front)
class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)


print('Deque')
d = Deque()
d.addFront('Hello')
d.addRear('World')
print(d.items)  # ['World', 'Hello']
print(d.size())  # 2
print(f'{d.removeFront()} {d.removeRear()}')  # 'Hello World'
print(d.isEmpty())  # True
