import sys

from cv2 import waitKey, imshow

from fulkerson import min_cut
from data import read_image_rgb

def main():
    image, seed = map(read_image_rgb, sys.argv[1:])

    img_fg, img_bg = segment_image(image, seed)

    imshow('ImageWindow', img_fg)
    waitKey()


if __name__ == '__main__':
    main()
