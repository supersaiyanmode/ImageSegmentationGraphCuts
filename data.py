import cv2
import numpy as np
from scipy.stats import multivariate_normal
from scipy.spatial.distance import euclidean

from node import Node
import constants
from edge import Edge


def read_image(path):
    return cv2.imread(path, 0)


def read_image_rgb(path):
    return cv2.imread(path)


def construct_nodes(image, image_seed):
    image = np.array(image)
    image_seed = np.array(image_seed)

    nrow, ncol, _ = image.shape
    node_map = {}

    # iterate over each node of image
    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            cur_position = rowIndex, colIndex

            intensity = image[cur_position]

            r, g, b = image_seed[cur_position]
            label = None

            # set to blue --> foreground
            if max(r, g) < 100 and b > 100:
                label = constants.FOREGROUND

            # set to blue --> background
            if max(g, b) < 100 and r > 100:
                label = constants.BACKGROUND

            node = Node(cur_position, intensity, label)
            node_map[cur_position] = node
    return node_map


def calc_fg_weight(node, gauss):
    if node.label == constants.FOREGROUND:
        return float("inf")
    return 1 - (gauss.pdf(gauss.mean) - gauss.pdf(node.intensity)) / gauss.pdf(gauss.mean)


def calc_bg_weight(node, gauss):
    if node.label == constants.BACKGROUND:
        return float("inf")
    return (gauss.pdf(gauss.mean) - gauss.pdf(node.intensity)) / gauss.pdf(gauss.mean)


def calc_weight(node, neighbor, max_dist=euclidean((0, 0, 0), (255, 255, 255))):
    return 1 - (euclidean(node.intensity, neighbor.intensity) / max_dist)


def construct_graph(image, image_seed):
    graph = construct_nodes(image, image_seed)

    mean, variance = stats(graph)
    gauss = multivariate_normal(mean=mean, cov=variance)

    fg_node = Node((-1, -1), None, "fg")
    bg_node = Node((-2, -2), None, "bg")

    for pos, node in graph.iteritems():
        adj_position = [(x[0]+y[0], x[1]+y[1]) for x, y in zip(constants.MOVES, [pos]*4)]
        neighbors = [graph[x] for x in adj_position if x in graph]

        fg_weight = calc_fg_weight(node, gauss)
        bg_weight = calc_bg_weight(node, gauss)

        fg_edge = Edge(node, fg_node, fg_weight)
        bg_edge = Edge(node, bg_node, bg_weight)

        edges = [Edge(node, x, calc_weight(node, x)) for x in neighbors]

    graph[fg_node.coord] = fg_node
    graph[bg_node.coord] = bg_node

    return graph, fg_node, bg_node


def split_pixels(graph):
    fg_pixels = [x.intensity for _, x in graph.iteritems() if x.label == constants.FOREGROUND]
    bg_pixels = [x.intensity for _, x in graph.iteritems() if x.label == constants.BACKGROUND]
    return fg_pixels, bg_pixels


def stats(graph):
    fg_pixels, bg_pixels = split_pixels(graph)

    cols = zip(*fg_pixels)
    mean = [x / float(y) for x, y in zip(map(sum, cols), map(len, cols))]
    variance = [sum(map(lambda x: x**2, y))/float(len(y)) for y in cols]
    variance = [x - y*y for x, y in zip(variance, mean)]

    var_mat = np.diag(variance)
    return mean, var_mat


def suppress_pixels(image, nodes):
    res = image.copy()
    for node in nodes:
        res[node.coord[0], node.coord[1], 0] = 0
        res[node.coord[0], node.coord[1], 1] = 0
        res[node.coord[0], node.coord[1], 2] = 0
    return res
