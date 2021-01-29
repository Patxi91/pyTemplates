

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


# Hashing for Ordered Search O(1)
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
print(h[1], h[2], h[3])  # one two three


# Sorting Data Structures
# https://www.toptal.com/developers/sorting-algorithms
# https://visualgo.net/en/sorting?slide=1


# Bubble Sort: O(n2): Each pass through the list places the next largest value in its proper place.
def bubble_sort(arr):
    for n in range(len(arr)-1, 0, -1):
        for k in range(n):
            if arr[k] > arr[k+1]:
                temp = arr[k]
                arr[k] = arr[k+1]
                arr[k+1] = temp


arr = [5, 3, 7, 2]
bubble_sort(arr)
print(arr)  # [2, 3, 5, 7]


# Selection Sort: O(n2): Improves the bubble sort by making only 1 exchange(largest value) every pass.
def selection_sort(arr):
    for fillslot in range(len(arr)-1, 0, -1):
        positionofmax = 0
        for location in range(1, fillslot+1):  # start in 1 since positionofmax = 0
            if arr[location] > arr[positionofmax]:
                positionofmax = location
        temp = arr[fillslot]
        arr[fillslot] = arr[positionofmax]
        arr[positionofmax] = temp


arr = [5, 8, 3, 10, 1]
selection_sort(arr)
print(arr)  # [1, 3, 5, 8, 10]


# Insertion Sort: O(n2): Maintains a sorted sublist and each time grows as the new item is inserted.
def insertion_sort(arr):
    for i in range(1, len(arr)):
        position = i
        currentvalue = arr[position]
        while position > 0 and arr[position-1] > currentvalue:
            arr[position] = arr[position - 1]
            position = position - 1
        arr[position] = currentvalue


arr = [4, 6, 2, 7, 4, 1, 9, 11, 23, 13, 2]
insertion_sort(arr)
print(arr)  # [1, 2, 2, 4, 4, 6, 7, 9, 11, 13, 23]


# Shell Sort: O(n2): Improves insertion sort by breaking the list into n increments and applying insertion to each.
def shell_sort(arr):

    sublistcount = len(arr)//2

    # While there are still sublists
    while sublistcount > 0:
        for start in range(sublistcount):
            # Use a gap insertion
            gap_insertion_sort(arr, start, sublistcount)

        sublistcount = sublistcount // 2


def gap_insertion_sort(arr, start, gap):

    for i in range(start+gap, len(arr), gap):

        position = i
        currentvalue = arr[position]

        # Using the Gap
        while position >= gap and arr[position-gap] > currentvalue:
            arr[position] = arr[position-gap]
            position = position-gap

        # Set current value
        arr[position] = currentvalue


arr = [4, 6, 2, 7, 4, 1, 9, 11, 23, 13, 2]
shell_sort(arr)
print(arr)  # [1, 2, 2, 4, 4, 6, 7, 9, 11, 13, 23]


# Merge Sort: O(n log(n)): Recursively splits a list in half, invokes a merge sort in both halves and merges them.
def merge_sort(arr):

    if len(arr) > 1:
        mid = len(arr) // 2
        lefthalf = arr[:mid]
        righthalf = arr[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)

        i = 0  # left
        j = 0  # right
        k = 0  # Merge

        # Merging
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                arr[k] = lefthalf[i]
                i += 1
            else:
                arr[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            arr[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            arr[k] = righthalf[j]
            j += 1
            k += 1


arr = [11, 2, 5, 4, 7, 56, 2, 12, 23]
merge_sort(arr)
print(arr)  # [2, 2, 4, 5, 7, 11, 12, 23, 56]


# Quick Sort: O(n): Chosen Pivot value(PV, 1st element) will find the split point.
# Concurrently will move other itmes greater or less than the pivot value. Leftmark > PV and Rightmark < PV will switch.
def quick_sort(arr):

    quick_sort_help(arr, 0, len(arr)-1)


def quick_sort_help(arr, first, last):

    if first < last:

        splitpoint = partition(arr, first, last)

        quick_sort_help(arr, first, splitpoint-1)  # Left half
        quick_sort_help(arr, splitpoint+1, last)  # Right half


def partition(arr, first, last):

    pivotvalue = arr[first]

    leftmark = first + 1
    rightmark = last

    done = False

    while not done:

        while leftmark <= rightmark and arr[leftmark] <= pivotvalue:
            leftmark += 1

        while arr[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark -= 1

        if rightmark < leftmark:
            done = True
        else:  # Exchange items
            temp = arr[leftmark]
            arr[leftmark] = arr[rightmark]
            arr[rightmark] = temp

    temp = arr[first]
    arr[first] = arr[rightmark]
    arr[rightmark] = temp

    return rightmark


arr = [2, 5, 4, 6, 7, 3, 1, 4, 12, 11]
quick_sort(arr)
print(arr)  # [1, 2, 3, 4, 4, 5, 6, 7, 11, 12]
