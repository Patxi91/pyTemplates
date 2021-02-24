import numpy as np
'''
Hallway Lockers:

Given a hallway lined with 100 lockers. Starting with one pass opening the lockers, so now their doors are opened out.
On a second pass, follow by closing every second locker.
Then, on a third go, close every third locker and close it if it is open or open it if it’s closed, "toggling" them.
Continue toggling every nth locker on pass number n.
After your hundredth pass of the hallway, in which you toggle only locker number 100, how many lockers are open?

Approach: Locker is only toggled when the pass number is a factor of the locker number.

- Locker 12
On pass 2: 2,4,6,8,10,12 (closed)
On pass 3: 3,6,9,12 (opened)
On pass 4: 4,8,12 (closed)
On pass 5: 5,10 No toggle on this pass
On pass 6: 6,12 (opened)
On pass 7: 7,14 No toggle on this pass
etc... then On pass 12: 12 (closed).

So lockers are closed if a locker is toggled an even number of times, it ends open otherwise.
Multiplication is a binary operation, so two numbers will always be involved.
But if the numbers are both the same number, a single number would be both halves of the pair --> odd number of factors.
ixi = n, therefore n must be a perfect square.
The perfect squares between 1 and 100 (inclusive) are 1, 4, 9, 16, 25, 36, 49, 64, 81, and 100.
So 10 lockers would remain open.
'''


# Unoptimized
def doors_unoptimized(m):
    doors = [False] * m  # Closed
    for i in range(100):
        for j in range(i, 100, i+1):
            doors[j] = not doors[j]
        print(f'Door {i+1}:', 'open' if doors[i] else 'close')
    return doors


ndoors = 100
doors = np.array(doors_unoptimized(ndoors))
print(f'From {ndoors}, a total of {np.sum(doors)} doors remain open.')  # From 100, a total of 10 doors remain open.


# Optimized: Only visits each door once








