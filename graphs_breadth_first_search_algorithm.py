from stacks_queues_and_deques import Queue
from graphs_algorithms import Vertex
from graphs_algorithms import Graph

# Breadth First Search (BFS) see MIT lecture: https://www.youtube.com/watch?v=s-CYnVz-uh4

'''
Applications:
- Web crawling
- Social Network behaviour
- Garbage collectors: Python, CPython, Java, etc...
- Model checking HW/SW --> Vertices are all states your program could reach
- Checking mathematical conjecture --> Vertices are all possible inputs to theorem
- Solving puzzles: 2x2 or 3x3 Rubik's Cube optimally

Note: BFS is like building a tree one level at a time. The parents pointers give the shortest path.

Keep track of progress: BFS here colors each of the vertices white, gray or black.
All vertices are initialized to white when they are constructed, a white vertex is an undiscovered vertex.
The BFS begins at the starting vertex 's' and color gray (currently explored). For 's', distance=0 and predecessor=None.
Start 's' is placed in a queue, next step is begin to explore vertices by iterating over its adjacency list.
When a vertex is initially discovered it is colored gray.
When BFS has completely explored a vertex, it is colored black.
'''


def bfs(g, start):

    # Initialize starting vertex and place it at the end of the queue
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)  # position 0

    while vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()  # Explore each vertex at the front of queue
        for nbr in currentVert.getConnections():  # Iterate over its adjacency list
            if nbr.getColor() == 'white':  # nbr --> new unexplored vertex that will be colored
                nbr.setColor('gray')  # Neighbor (nbr) initially explored
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)  # Add nbr to end of queue for later exploration --> self.items.insert(0, item)
        currentVert.setColor('black')  # Completely explored --> No white vertices adjacent to it
