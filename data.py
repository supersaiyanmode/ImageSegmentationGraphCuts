import math

import cv2
import numpy as np
from scipy.stats import multivariate_normal

from node import Node
import constants
from edge import Edge
import config

def read_image(path):
    return cv2.imread(path, 0)

def read_image_rgb(path):
    return cv2.imread(path)

def construct_nodes(image, image_seed):
    image = np.array(image)
    image_seed = np.array(image_seed)

    nrow, ncol, _ = image.shape
    nodeMap = {}

    # iterate over each node of image
    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            currPosition = rowIndex, colIndex

            intensity = image[currPosition]

            r, g, b = image_seed[currPosition]
            label = None

            # set to blue --> foreground
            if max(r, g) < 100 and b > 100:
                label = constants.FOREGROUND

            # set to blue --> background
            if max(g, b) < 100 and r > 100:
                label = constants.BACKGROUND

            node = Node(currPosition, intensity, label)
            nodeMap[currPosition] = node
    return nodeMap


def calc_fg_weight(node, gauss):
    if node.label == constants.FOREGROUND:
        return float("inf")
    return math.log(gauss.pdf(node.intensity))

def calc_bg_weight(node):
    if node.label == constants.BACKGROUND:
        return float("inf")
    return config.background_cost

def calc_weight(node, neighbor):
    return None

def construct_edges(graph):
    mean, variance = stats(graph)
    gauss = multivariate_normal(mean=mean, cov=variance)

    fg_node = Node((-1, -1), None, "fg")
    bg_node = Node((-2, -2), None, "bg")

    for pos, node in graph.iteritems():
        adj_position = [(x[0]+y[0], x[1]+y[1]) for x, y in zip(constants.MOVES, [pos]*4)]
        neighbors = [graph[x] for x in adj_position if x in graph]

        edges = [Edge(node, x, calc_weight(node, x)) for x in neighbors]

        fg_weight = calc_fg_weight(node, gauss)
        bg_weight = calc_bg_weight(node)

        fg_edge = Edge(node, fg_node, fg_weight)
        bg_edge = Edge(node, bg_node, bg_weight)


def split_pixels(graph):
    fg_pixels = [x.intensity for _, x in graph.iteritems() if x.label == constants.FOREGROUND]
    bg_pixels = [x.intensity for _, x in graph.iteritems() if x.label == constants.BACKGROUND]
    return fg_pixels, bg_pixels

def stats(graph):
    fg_pixels, bg_pixels = split_pixels(graph)

    cols = zip(*fg_pixels)
    mean = [x/float(y) for x,y in zip(map(sum, cols), map(len, cols))]
    variance = [sum(map(lambda x: x**2, y))/float(len(y)) for y in cols]
    variance = [x - y*y for x,y in zip(variance, mean)]

    var_mat = np.diag(variance)
    return mean, variance

def main():
    nara = read_image_rgb('dataset/nara.png')
    nara_seed = read_image_rgb('dataset/nara-seeds.png')
    graph = construct_nodes(nara, nara_seed)
    construct_edges(graph)

if __name__ == '__main__':
    main()

