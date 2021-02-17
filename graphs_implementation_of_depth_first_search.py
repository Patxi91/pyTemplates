
'''
DFS: https://jeremykun.com/2013/01/22/depth-and-breadth-first-search/

Explores possible vertices (from a supplied root) down each branch before backtracking.
This property allows the algorithm to be implemented succinctly in both iterative and recursive forms.
Upon each visit to a node:
    1.Mark the current vertex as being visited.
    2.Explore each adjacent vertex that is not included in the visited set.
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


# Iterative form

def dfs_i(graph, start):
    visited = set()  # set of already visited vertices
    stack = [start]  # pipeline of vertices to be visited
    while stack:
        vertex = stack.pop()  # treated as a stack --> pops off at the end
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)  # graph['A'] = set(['B', 'C']) --> set(['B', 'C']) - set ('A'). Using Python’s overloading of the subtraction operator.
    return visited


print(dfs_i(graph, 'A'))  # {'A', 'B', 'C', 'D', 'E', 'F'}


# Recursive form

def dfs_r(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for nxt in graph[start] - visited:
        dfs_r(graph, nxt, visited)  # variables passed by reference
    return visited


print(dfs_r(graph, 'A'))  # {'A', 'B', 'C', 'D', 'E', 'F'}


# Paths - return all possible paths between a start and goal vertex.

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for nxt in graph[vertex] - set(path):
            if nxt == goal:
                yield path + [nxt]
            else:
                stack.append((nxt, path + [nxt]))


print(list(dfs_paths(graph, 'A', 'F')))  # [['A', 'B', 'E', 'F'], ['A', 'C', 'F']]
