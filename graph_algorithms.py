# Graph: Set of vertices and set of edges with weights. G=(V,E), where V={V0,..., Vn} and E={(V0,V1,x),..., (Vn,Vn-i,y)}
class Vertex:

    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def add_neighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def get_connections(self):
        return self.connectedTo.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ' connected to: ' + str([x.id for x in self.connectedTo])







