from graphs_algorithms import Graph

'''
The Knight's tour puzzle is played ona chess board with a single knight.
Objective is to find a sequence of moves that allow the knight to visit
every square on the board exactly once.

Approach: Depth First Search (DFS).

As opposed to a breadth first search (BFS) algorithm that builds a search tree one level at a time,
the DFS creates a search tree exploring one branch of the tree as deeply as possible,
until there are no moves possible, then it backs up the tree to the next deepest vertex that allows a legal move.
'''


def knightGraph(bdSize):
    ktGraph = Graph()
    for row in range(bdSize):
        for col in range(bdSize):
            nodeId = posToNodeId(row,col,bdSize)
            newPositions = genLegalMoves(row,col,bdSize)
            for e in newPositions:
                nid = posToNodeId(e[0],e[1],bdSize)
                ktGraph.addEdge(nodeId,nid)
    return ktGraph


def posToNodeId(row, column, board_size):
    return (row * board_size) + column


def genLegalMoves(x,y,bdSize):
    newMoves = []
    moveOffsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),
                   ( 1,-2),( 1,2),( 2,-1),( 2,1)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX,bdSize) and \
                        legalCoord(newY,bdSize):
            newMoves.append((newX,newY))
    return newMoves


def legalCoord(x,bdSize):
    if x >= 0 and x < bdSize:
        return True
    else:
        return False


def knightTour(n, path, u, limit):
    """
    :param n: current depth in the search tree
    :param path: list of vertices visited up to this point
    :param u: the vertex in the graph we wish to explore
    :param limit: the number of nodes in the path
    :return:
    """

    u.setColor('gray')
    path.append(u)
    if n < limit:
        nbrList = list(u.getConnections())
        i = 0
        done = False
        while i < len(nbrList) and not done:
            if nbrList[i].getColor() == 'white':
                done = knightTour(n + 1, path, nbrList[i], limit)
            i = i + 1
        if not done:  # prepare backtrack --> sets vertices below next deepest vertex allowing a legal move white again
            path.pop()
            u.setColor('white')
    else:
        done = True  # backtrack
    return done
