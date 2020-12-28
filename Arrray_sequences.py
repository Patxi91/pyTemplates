import sys

# Array Sequences
# List: [1,2,3], Tuple: (1,2,3), String: '123'

arr = [0]*5  # arr = [0,0,0,0,0] where each index points to the same memory address.
print(id(arr[0]) == id(arr[1]))

# Dynamic Arrays
n = 10
data = []
for i in range(n):
    a = len(data)  # Number of Data
    b = sys.getsizeof(data)  # Actual Size in Bytes
    print(f'Length: {a}, Size: {b}')
    data.append(n)  # Increase Size by one

# Dynamic array implementation




