from PIL import Image
import requests
from io import BytesIO

'''
Jugs of Water:

Having a five gallons jug and a three gallons jug, and an unlimited supply of water (but no measuring cups).
What is the minimum number of steps to come up exactly with four gallons of water?
'''

# Show approach
url = 'http://mindyourdecisions.com/blog/wp-content/uploads/2013/02/water-jug-riddle-1.png'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()


def gcd(a, b):
    if b== 0:
        return a
    return gcd(b, a % b)


''' fromCap -- Capacity of jug from which
              water is poured
   toCap   -- Capacity of jug to which
              water is poured
   d       -- Amount to be measured '''


def pour(toJugCap, fromJugCap, d):
    # Initialize current amount of water in source and destination jugs
    fromJug = fromJugCap
    toJug = 0

    # Initialize steps required
    step = 1
    while fromJug != d and toJug != d:

        # Find the maximum amount that can be poured
        temp = min(fromJug, toJugCap - toJug)

        # Pour 'temp' liter from 'fromJug' to 'toJug'
        toJug = toJug + temp
        fromJug = fromJug - temp

        step = step + 1
        if fromJug == d or toJug == d:
            break

        # If first jug becomes empty, fill it
        if fromJug == 0:
            fromJug = fromJugCap
            step = step + 1

        # If second jug becomes full, empty it
        if toJug == toJugCap:
            toJug = 0
            step = step + 1

    return step


# Returns count of minimum steps needed to measure d liter
def minSteps(n, m, d):
    if m > n:
        temp = m
        m = n
        n = temp

    if d % gcd(n, m) != 0:
        return -1

    # Return minimum two cases: Water of n liter jug is poured into m liter jug
    return min(pour(n, m, d), pour(m, n, d))


# Driver code
if __name__ == '__main__':
    n = 3
    m = 5
    d = 4

    print(f'Minimum number of steps required is {minSteps(n, m, d)}')  # Minimum number of steps required is 6
