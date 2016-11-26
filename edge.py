import utils

class Edge:
    def __init__(self, node1, node2):
        # calculate weight energy between n1 node and n2!
        self.node1 = node1
        self.node2 = node2
        self.weight = utils.weight(node1, node2)

    def get_other(self, node):
        if self.node1 == node:
            return self.node2
        return self.node1
