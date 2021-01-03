from nose.tools import assert_equal

'''
Implement a Queue - Using Two Stacks:
Given the Stack class below, implement a Queue class using two stacks!
Note, use a Python list data structure as your Stack.
# Uses lists instead of your own Stack class.
stack1 = []
stack2 = []
'''


class Queue2Stacks:

    def __init__(self):

        # Two Stacks
        self.in_stack = []
        self.out_stack = []

    def enqueue(self, element):
        self.in_stack.append(element)
        pass

    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()
        pass


class Test:
    def test(self, sol):
        n = 5
        for i in range(n):
            q.enqueue(i)
        for i in range(n):
            assert_equal(q.dequeue(), i)
            print(i)
        print('ALL TEST CASES PASSED')


# Run Tests
q = Queue2Stacks()
t = Test()
t.test(Queue2Stacks())
