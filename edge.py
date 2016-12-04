
class Edge(object):
    def __init__(self, node1, node2, capacity):
        self.node1, self.node2 = sorted([node1, node2], key=lambda x: x.coord)
        self.capacity = capacity
        self.residual = capacity

        self._connect(node1, node2)

    def _connect(self, node1, node2):
        node1.edges.add(self)
        node2.edges.add(self)

    def get_other(self, node):
        if self.node1 == node:
            return self.node2
        return self.node1

    def __hash__(self):
        return hash((self.node1.coord, self.node2.coord))

    def __eq__(self, other):
        return self.node1.coord == self.node2.coord

    def __repr__(self):
        return str(self.node1) + "-" + str(self.residual) + "-" + str(self.node2)
