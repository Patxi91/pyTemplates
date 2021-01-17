

# Sequential Search Unordered List O(n)
def seq_search(arr, ele):
    pos = 0
    found = False

    while pos < len(arr) and not found:
        if arr[pos] == ele:
            found = True
        else:
            pos += 1
    return found


arr = [1, 2, 3, 4, 5]
print(seq_search(arr, 3))  # True


# Sequential Search Ordered List O(n)
def ordered_seq_search(arr, ele):
    pos = 0
    found = False
    stopped = False

    while pos < len(arr) and not found and not stopped:
        if arr[pos] == ele:
            found = True
        else:
            if arr[pos] > ele:
                stopped = True
            else:
                pos += 1
    return found


arr = [1, 2, 3, 4, 5]
print(seq_search(arr, 2))  # True


# Binary Search O(log2 (n))
def binary_search(arr, ele):
    first = 0
    last = len(arr)-1
    found = False

    while first <= last and not found:
        mid = (first+last) // 2
        if arr[mid] == ele:
            found = True
        else:
            if ele < arr[mid]:
                last = mid-1  # use lower half
            else:
                first = mid+1  # use upper half
    return found


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(binary_search(arr, 7))  # True


# Recursive Version of Binary Search
def rec_bin_search(arr, ele):
    if len(arr) == 0:  # was never found
        return False
    else:
        mid = len(arr) // 2
        if arr[mid] == ele:
            return True
        else:
            if ele < arr[mid]:
                return rec_bin_search(arr[:mid], ele)
            else:
                return rec_bin_search(arr[mid+1:], ele)


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(rec_bin_search(arr, 7))  # True


# Hashing for ordered search O(1)
class HashTable:
    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, data):
        hashvalue = self.hashfunction(key, len(self.slots))
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] == data
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))
                while self.slots[nextslot] != None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot, len(self.slots))
                if self.slots[nextslot] == None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data

    def hashfunction(self, key, size):
        return key % size

    # Linear Probing
    def rehash(self, oldhash, size):
        return (oldhash + 1) % size

    def get(self, key):
        startslot = self.hashfunction(key, len(self.slots))
        data = None
        stop = False
        position = startslot
        while self.slots[startslot] != None and not stop:
            if self.slots[position] == key:
                stop = True
                data = self.data[position]
            else:
                position = self.rehash(position, len(self.slots))
                if position == startslot:
                    stop = True
        return data

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)


h = HashTable(5)
h[1] = 'one'
h[2] = 'two'
h[3] = 'three'






















