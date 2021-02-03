# Graph: Set of vertices and set of edges with weights. G=(V,E), where V={V0,..., Vn} and E={(V0,V1,x),..., (Vn,Vn-i,y)}
class Vertex:

    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def add_neighbor(self, nbr, weight=0):  # called by Graph().add_edge
        self.connectedTo[nbr] = weight

    def get_connections(self):
        return self.connectedTo.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ' connected to: ' + str([x.id for x in self.connectedTo])


class Graph:

    def __init__(self):
        self.vertList = {}  # Adjacency List dictionary
        self.numVertices = 0

    def add_vertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def get_vertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def add_edge(self, fv, tv, weight=0):
        if fv not in self.vertList:
            nv = self.add_vertex(fv)
        if tv not in self.vertList:
            nv = self.add_vertex(tv)
        self.vertList[fv].add_neighbor(self.vertList[tv], weight)  # calls Vertex().add_neighbor

    def get_vertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def __contains__(self, item):
        return item in self.vertList


# Driver

g = Graph()

for i in range(6):
    g.add_vertex(i)

print(g.vertList)  # {0: <__main__.Vertex object at 0x04047928>, 1: <__main__.Vertex object at 0x04047520>, 2: <__main__.Vertex object at 0x040479A0>, 3: <__main__.Vertex object at 0x04047AC0>, 4: <__main__.Vertex object at 0x04047AD8>, 5: <__main__.Vertex object at 0x04047988>}

g.add_edge(0, 1, 2)
for vertex in g:  # Uses special method __iter__(self)
    print(vertex)  # 0 connected to: [1]
    print(vertex.get_connections())  # dict_keys([<__main__.Vertex object at 0x036CD328>])

