import contants

class Node:
    def __init__(self, node, intensity, x, y):
        self.node = node
        self.x = x
        self.y = y
        self.intensity = intensity

        # left, right, top and bottom edges
        self.edges = [None] * contants.NUMBER_OF_EDGES

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def setRight(self, other):
        self.edges[contants.RIGHT] = other

    def getRight(self):
        return self.edges[contants.RIGHT]

    def setLeft(self, other):
        self.edges[contants.LEFT] = other

    def getLeft(self):
        return self.edges[contants.LEFT]

    def setTop(self, other):
        self.edges[contants.TOP] = other

    def getTop(self):
        return self.edges[contants.TOP]

    def setBottom(self, other):
        self.edges[contants.BOTTOM] = other

    def getBottom(self):
        return self.edges[contants.BOTTOM]




