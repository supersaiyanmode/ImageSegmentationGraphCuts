import constants


class Node(object):
    def __init__(self, coord, intensity, label):
        self.label = label
        self.coord = coord
        self.intensity = intensity
        self.value = self.to_grayscale(self.intensity) \
                if self.intensity is not None else None
        self.edges = set()
    
    def to_grayscale(self, rgb):
        return rgb

    def get_neighbors(self):
        return [x.get_other(self) for x in self.edges]

    def is_bg(self):
        return self.label == "bg"

    def is_fg(self):
        return self.label == "fg"

