import cv2
import numpy as np
from node import Node
import constants
import utils
from edge import Edge

def read_image(path):
    return cv2.imread(path, 0)

def read_image_rgb(path):
    return cv2.imread(path)

def create_graph(image, image_seed):
    image = np.array(image)
    image_seed = np.array(image_seed)

    nrow, ncol = image.shape
    print nrow, ncol
    # check node is already created
    # nodeMap = np.zeros(image.shape)
    nodeMap = dict()

    # iterate over each node of image
    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            currPosition = (rowIndex, colIndex)

            intensity = image[currPosition]

            r, g, b = image_seed[currPosition]
            label = None

            # set to blue --> foreground
            if max(r, g) < 100 and b > 100:
                label = 0

            # set to blue --> background
            if max(g, b) < 100 and r > 100:
                label = 1

            node = Node(intensity, label, rowIndex, colIndex)
            nodeMap[currPosition] = node

            # check the four neighboring pixels - Also, check if it is a valid move
            # check if adjacent nodes are created
            for moveIndex in xrange(len(constants.MOVES)):
                adjPosition = tuple([sum(x) for x in zip(constants.MOVES[moveIndex], currPosition)])
                # check if it is a valid coordinate
                if utils.isValidMove(adjPosition, nrow, ncol) and adjPosition in nodeMap:
                    adjNode = nodeMap[adjPosition]
                    # create an edge
                    edge = Edge(node, adjNode)

                    # make this better looking..!!
                    if moveIndex == constants.LEFT:
                        node.setLeft(edge)
                        adjNode.setRight(edge)
                    elif moveIndex == constants.RIGHT:
                        node.setRight(edge)
                        adjNode.setLeft(edge)
                    elif moveIndex == constants.TOP:
                        node.setTop(edge)
                        adjNode.setBottom(edge)
                    elif moveIndex == constants.BOTTOM:
                        node.setBottom(edge)
                        adjNode.setTop(edge)
    return nodeMap

def compute_mean_variance(image, image_seed):
    image = np.array(image)
    image_seed = np.array(image_seed)

    nrow, ncol = image.shape
    print nrow, ncol

    count = [0.0 for _ in xrange(constants.CLASSIFICATION_TYPE)]

    mean = [[0.0 for _ in xrange(constants.CLASSIFICATION_TYPE)] for _ in xrange(constants.NUMBER_OF_COLORS)]
    var = [[0.0 for _ in xrange(constants.CLASSIFICATION_TYPE)] for _ in xrange(constants.NUMBER_OF_COLORS)]
    # iterate over each node of image
    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            currPosition = (rowIndex, colIndex)
            rgb = image_seed[currPosition]
            r, g, b = rgb
            label = None

            # set to blue --> foreground
            if max(r, g) < 100 and b > 100:
                count[constants.FOREGROUND] += 1
                label = constants.FOREGROUND

            # set to blue --> background
            if max(g, b) < 100 and r > 100:
                count[constants.BACKGROUND] += 1
                label = constants.BACKGROUND

            for colorIndex in xrange(constants.NUMBER_OF_COLORS):
                mean[label][colorIndex] += rgb[colorIndex]
                var[label][colorIndex] = pow(rgb[colorIndex], 2)

    for colorIndex in xrange(constants.NUMBER_OF_COLORS):
        for labelIndex in xrange(constants.CLASSIFICATION_TYPE):
            mean[labelIndex][colorIndex] /= count[labelIndex]
            var[labelIndex][colorIndex] = var[labelIndex][colorIndex]/count[labelIndex] - \
                pow(mean[labelIndex][colorIndex], 2)

    return mean, var

def main():
    nara = read_image('dataset/nara.png')
    nara_seed = read_image_rgb('dataset/nara-seeds.png')
    create_graph(nara, nara_seed)

if __name__ == '__main__':
    main()