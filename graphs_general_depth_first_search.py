from graphs_algorithms import Graph

'''
General Depth First Search (DFS):
Search as deep as possible, connecting as many nodes in the graph as possible, branching when necessary.

The predecessor links (parents pointers) are used to construct the tree.
:param: Discovery time: Tracks the number of steps in the algorithm before a vertex is first encountered,
:param: Finish time: Number of steps in the algorithm before a vertex is colored black
'''


class DFSGraph(Graph):

    def __init__(self):
        super().__init__()
        self.time = 0

    def dfs(self):
        for aVertex in self:  # self --> instance of DFSGraph class
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex)

    def dfsvisit(self, startVertex):
        startVertex.setColor('gray')
        self.time += 1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
        startVertex.setColor('black')
        self.time += 1
        startVertex.setFinish(self.time)







