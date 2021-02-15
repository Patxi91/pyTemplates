# Breadth First Search (BFS) see MIT lecture: https://www.youtube.com/watch?v=s-CYnVz-uh4
'''
Applications:
- Web crawling
- Social Network behaviour
- Garbage collectors: Python, Cpython, Java, etc...
- Model checking HW/SW --> Vertices are all states your program could reach
- Checking mathematical conjecture --> Vertices are all possible inputs to theorem
- Solving puzzles: 2x2 or 3x3 Rubik's Cube optimally

Note: BFS is like building a tree one level at a time. The parents pointers give the shortest path.

Keep track of progress: BFS colors each of the vertices white, gray or black.
All vertices are initialized to white when they are constructed, a white vertex is an undiscovered vertex.
The BFS begins at the starting vertex 's' and color gray (currently explored). For 's', distance=0 and predecessor=None.
Start 's' is placed in a queue, next step is begin to explore vertices by iterating over its adjacency list.
When a vertex is initially discovered it is colored gray.
When BFS has completely explored a vertex, it is colored black.
'''


