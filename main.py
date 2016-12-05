import sys
import time

from cv2 import waitKey, imshow, imwrite

from data import read_image_rgb
from segment import naive_segment_image
from segment import segment_image
from fulkerson import min_cut as min_cut_fulkerson
from bidirectional import min_cut as min_cut_bidirectional
import config


def main():
    start = time.time()

    image, seed = map(read_image_rgb, sys.argv[1:])

    algorithm = {
        "fulkerson": min_cut_fulkerson,
        "bidirectional": min_cut_bidirectional
    }[config.algorithm]

    img_fg1, img_bg1 = naive_segment_image(image, seed)
    img_fg2, img_bg2 = segment_image(algorithm, image, seed)

    end = time.time()
    base = sys.argv[1].replace(".png", "").replace("dataset/","")
    base = "output/" + base

    with open(base + ".time.txt", "w") as f:
        print>> f, (end - start)

    imwrite(base + "-fg-naive.png", img_fg1)
    imwrite(base + "-bg-naive.png", img_bg1)
    imwrite(base + "-fg-gc.png", img_fg2)
    imwrite(base + "-bg-gc.png", img_bg2)

    if config.show_result:
        imshow('Foreground-Naive', img_fg1)
        imshow('Background-Naive', img_bg1)
        imshow('Foreground-GC', img_fg2)
        imshow('Background-GC', img_bg2)
        waitKey()


if __name__ == '__main__':
    main()
