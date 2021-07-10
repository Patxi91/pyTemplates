import time


def my_generator(x=1):  # Every time we call this function, x is saved from the previous time.
    """Like a function but it never closes (due to yield)"""
    while True:
        yield x  # Tells Python to keep the function open and save all the
        x += 1


gene = my_generator()

gene = my_generator()
print(type(gene))

for i in gene:
    print(i, end=' ')
    time.sleep(0.5)
