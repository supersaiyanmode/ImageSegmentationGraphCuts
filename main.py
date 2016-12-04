import sys

from cv2 import waitKey, imshow, imwrite

from data import read_image_rgb
from fulkerson import naive_segment_image
from fulkerson import segment_image

def main():
    image, seed = map(read_image_rgb, sys.argv[1:])

    img_fg1, img_bg1 = naive_segment_image(image, seed)
    img_fg2, img_bg2 = segment_image(image, seed)

    imshow('Foreground', img_fg)
    imshow('Background', img_bg)
    waitKey()


if __name__ == '__main__':
    main()
