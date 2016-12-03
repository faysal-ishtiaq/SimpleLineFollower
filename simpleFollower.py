__author__ = "f.i.rabby@gmail.com"

import cv2
import numpy as np

stroke_width    = 3
radius          = 3
blue            = [255, 0, 0]
green           = [0, 255, 0]
red             = [0, 0, 255]

def main():
    # Load an color image
    img_color = cv2.imread('sample.jpg')

    #convert it to gray
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    #get height and width
    height, width = img.shape

    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    right_edge = int(lines[0][0][0])
    left_edge = int(lines[1][0][0]) + 1

    #draw circle on image center
    img_color = cv2.circle(img_color, (int(width / 2), int(height / 2)), radius, green, stroke_width)

    #draw circle on the left edge
    img_color = cv2.circle(img_color, (left_edge, int(height / 2)), radius, red, stroke_width)

    #draw circle on the right edge
    img_color = cv2.circle(img_color, (right_edge, int(height / 2)), radius, red, stroke_width)

    line_center_x = right_edge - (int((right_edge - left_edge) /2))

    #draw circle on the line center
    img_color = cv2.circle(img_color, (int(line_center_x), int(height / 2)), radius, blue, stroke_width)

    move = int(width/2 - line_center_x);

    if move > 0:
        dir = 'right'
    elif move < 0:
        dir = 'left'
    else:
        dir = 'null'

    print("move", move, "px", dir)

    cv2.imshow('lines_color', img_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
