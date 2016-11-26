import cv2
import numpy as np

def read_image(path):
    return cv2.imread(path, 0)

def create_graph(image, image_seed):
    # create a graph
    pass

def main():
    nara = read_image('dataset/nara.png')
    nara_seed = read_image('dataset/nara-seeds.png')

if __name__ == '__main__':
    main()