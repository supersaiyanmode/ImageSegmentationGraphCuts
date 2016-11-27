import constants

class Node:
    def __init__(self, intensity, label, x, y):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.label = label

        # left, right, top and bottom edges
        self.edges = [None] * constants.NUMBER_OF_EDGES

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def setRight(self, other):
        self.edges[constants.RIGHT] = other

    def getRight(self):
        return self.edges[constants.RIGHT]

    def setLeft(self, other):
        self.edges[constants.LEFT] = other

    def getLeft(self):
        return self.edges[constants.LEFT]

    def setTop(self, other):
        self.edges[constants.TOP] = other

    def getTop(self):
        return self.edges[constants.TOP]

    def setBottom(self, other):
        self.edges[constants.BOTTOM] = other

    def getBottom(self):
        return self.edges[constants.BOTTOM]




