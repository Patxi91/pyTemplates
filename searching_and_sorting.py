

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

























