# Big-O:
# https://stackoverflow.com/questions/487258/what-is-a-plain-english-explanation-of-big-o-notation/487278#487278
# https://stackoverflow.com/questions/487258/what-is-a-plain-english-explanation-of-big-o-notation/487278#487278

# O(1) Constant
def func_constant(values):
    print(values[0])
list = [1,2,3,4,5]
func_constant(list)

# O(n) Linear
def func_linear(list):
    for val in list:
        print(val)
def func_linear2(list): #O(2n) --> O(n)
    for val in list:
        print(val)
    for val in list:
        print(val)
list = [1,2,3,4,5]
func_linear(list)

# O(n^2) Quadratic
def func_quad(list):
    for i in list:
        for j in list:
            print(i,j)
list = [1,2,3,4,5]
func_quad(list)

# Big-O case1
def func_complex(list):
    print(list[0])  # O(1)
    ###  O(n/2)
    midpoint = int(len(list)/2)
    for val in list[:midpoint]:
        print(val)
    ###
    for x in range(10):  # O(10)
        print('Hello World')
list = [1,2,3,4,5,6,7,8,9,10]
func_complex(list)  # Overal O: O(1+ n/2 + 10) --> O(n)

# Big-O case2
def matcher(list, match):
    for item in list:
        if item == match:
            return True
    return False
list = [1,2,3,4,5,6,7,8,9,10]
print(matcher(list,1))  # O(1)
print(matcher(list,11))  # O(n)


# Space complexity
def create_list(n):
    new_list = []
    for i in range(n):
        new_list.append('new')
    return new_list
print(create_list(10))  # O(n) in terms of Space complexity

def printer(n):
    for i in range(10):  # Time complexity O(n)
        print('Hello World!')  # Space complexity O(1)
printer(10)


# Big O for Python Data Structures
def method1():
    l = []
    for n in xrange(10000):
        l = l + [n]
def method2():
    l = []
    for n in xrange(10000):
        l.append(n)
def method3():
    l = [n for n in xrange(10000)]
def method4():
    l = range(10000) # Python 3: list(range(10000))