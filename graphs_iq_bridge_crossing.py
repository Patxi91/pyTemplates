
'''
Bridge Crossing:
A group of four travelers comes to a bridge at night.
The bridge can hold the weight of at most only two of the travelers at a time.
The bridge cannot be crossed without using a flashlight, and the travelers have one flashlight among them.
Each traveler walks at a different speed: The first can cross the bridge in 1 minute, the second in 2 minutes, the third in 5 minutes, and the fourth takes 10 minutes to cross the bridge.
If two travelers cross together, they walk at the speed of the slower traveler.

What is the least amount of time in which all the travelers can cross from one side of the bridge to the other?

See:
https://en.wikipedia.org/wiki/River_crossing_puzzle
https://en.wikipedia.org/wiki/Bridge_and_torch_problem


Move [Time]
(1) & (2) Cross with Torch	[2]
(1) Returns with Torch	[1]
(5) & (10) Cross with Torch	[10]
(2) Returns with Torch	[2]
(1) & (2) Cross with Torch	[2]
Total [17]
'''

# Approach: https://page.mi.fu-berlin.de/rote/Papers/pdf/Crossing+the+bridge+at+night.pdf
f = lambda s: s[0] + s[-1] + min(2*s[1], s[0]+s[-2]) + f(s[:-2]) if s.sort() or 3 < len(s) else sum(s[len(s) == 2:])

print(f([1,2,5,10]))  # 17
