import sys

from cv2 import waitKey, imshow, imwrite

from data import read_image_rgb
from fulkerson import naive_segment_image
from fulkerson import segment_image
import config

def main():
    image, seed = map(read_image_rgb, sys.argv[1:])

    img_fg1, img_bg1 = naive_segment_image(image, seed)
    img_fg2, img_bg2 = segment_image(image, seed)

    imwrite("fg-naive.png", img_fg1)
    imwrite("bg-naive.png", img_bg1)
    imwrite("fg-gc.png", img_fg2)
    imwrite("bg-gc.png", img_bg2)

    if config.show_result:
        imshow('Foreground-Naive', img_fg1)
        imshow('Background-Naive', img_bg1)
        imshow('Foreground-GC', img_fg2)
        imshow('Background-GC', img_bg2)
        waitKey()


if __name__ == '__main__':
    main()
