# BFS = Same results as DFS but with the added guarantee to return the shortest-path first.

'''
The actions performed per each explored vertex are the same as the depth-first implementation.
Replacing the stack with a queue will instead explore the breadth of a vertex depth before moving on.
This way, the first path located is one of the shortest-paths present, based on number of edges being the cost factor.
Assume the following simplified version of the graph:
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}
'''

graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}


def bfs(graph, start):
    '''
    Similar to DFS, but removes the next item from the beginning of the list structure queue instead of the stacks last.
    '''
    visited = set()
    queue = [start]
    while queue:
        vertex = queue.pop(0)  # treated as a queue --> pops off at the beginning
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited


print(bfs(graph, 'A'))  # {'A', 'B', 'C', 'D', 'E', 'F'}


# Paths - return all possible paths between a start and goal vertex.

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


print(list(bfs_paths(graph, 'A', 'F')))  # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]


# Shortest path method:  returns the shortest path found or ‘None’ if no path exists.

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


print(shortest_path(graph, 'A', 'F'))  # ['A', 'C', 'F']
