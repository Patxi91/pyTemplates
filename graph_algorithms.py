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
        self.vertList[fv].add_neighbor(tv, weight)  # calls Vertex().add_neighbor










