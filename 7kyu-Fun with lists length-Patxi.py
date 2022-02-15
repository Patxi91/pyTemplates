def length(head):
    if not head:
        return 0
    count = 0
    while head.next:
        count, head = count + 1, head.next
    return count+1
