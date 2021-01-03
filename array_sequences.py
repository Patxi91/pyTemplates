import sys
import ctypes

# Array Sequences
# List: [1,2,3], Tuple: (1,2,3), String: '123'

arr = [0]*5  # arr = [0,0,0,0,0] where each index points to the same memory address.
print(id(arr[0]) == id(arr[1]))

# Dynamic arrays memory allocation
n = 10
data = []
for i in range(n):
    a = len(data)  # Number of Data
    b = sys.getsizeof(data)  # Actual Size in Bytes
    print(f'Length: {a}, Size: {b}')
    data.append(n)  # Increase Size by one


# Dynamic array implementation
    '''
    DYNAMIC ARRAY CLASS (Similar to Python List)
    '''


class DynamicArray(object):
    def __init__(self):
        self.n = 0
        self.capacity = 1
        self.A = self.make_array(self.capacity)

    def __len__(self):
        return self.n

    def __getitem__(self, k):
        if not 0 <= k < self.n:
            return IndexError('k is out of bounds')
        return self.A[k]

    def append(self, ele):
        """
        Add element to end of the array
        """
        if self.n == self.capacity:
            self._resize(2*self.capacity)  # 2x if capacity isn't enough (Amortization)
        self.A[self.n] = ele
        self.n += 1

    def _resize(self, new_cap):
        """
        Resize internal array to capacity new_cap
        """
        B = self.make_array(new_cap)
        for k in range(self.n):
            B[k] = self.A[k]
        self.A = B
        self.capacity = new_cap

    def make_array(self, new_cap):
        """
        Returns a new array with new_cap capacity
        """
        return (new_cap * ctypes.py_object)()


arr = DynamicArray()
n = 10
for i in range(n):
    a = len(arr)  # Number of Data
    b = ctypes.sizeof(arr.A)  # sys.getsizeof(arr.A) just returns the garbage collector overhead
    print(f'Dynamic array Length: {a}, Size: {b}')
    arr.append(n)
