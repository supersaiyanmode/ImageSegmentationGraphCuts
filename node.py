
class Node(object):
    def __init__(self, coord, intensity, label):
        self.label = label
        self.coord = coord
        self.intensity = intensity
        self.edges = set()

    def get_neighbors(self):
        return [x.get_other(self) for x in self.edges]

    def is_bg(self):
        return self.label == "bg"

    def is_fg(self):
        return self.label == "fg"

    def __repr__(self):
        return "Node:" + str(self.coord)
