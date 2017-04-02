from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2
import motor

def decide(count):
    if white(count[1][1]) and white(count[2][1]):
        if(white(count[2][0]) and white(count[2][2])):
            print("start")
            #motor.forward(1)
        elif(white(count[0][0]) and white(count[0][2])):
            print("stop")
            #motor.stop(500)
        elif(white(count[1][0])):
            print("left")
            #motor.left(1)
        elif(white(count[1][2])):
            print("right")
            #motor.right(1)
        elif(white(count[0][1])):
            print("forward")
            #motor.forward(1)
        else:
            print("if, else")
    else:
        print("else")


def takeAction(count):
    if white(count[1][1]) and white(count[2][1]):
        if(white(count[2][0]) and white(count[2][2])):
            print("start")
            motor.forward(1)
        elif(white(count[0][0]) and white(count[0][2])):
            print("stop")
            motor.stop(500)
        elif(white(count[1][0])):
            print("left")
            motor.left(1)
        elif(white(count[1][2])):
            print("right")
            motor.right(1)
        elif(white(count[0][1])):
            print("forward")
            motor.forward(1)
        else:
            print("else, else")
    else:
        print("else")


def white(perc):
    return perc > 0.25

def orderPoints(pts):
    rect = np.zeros((4,2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def fourPointTransform(image, pts):
    rect = orderPoints(pts)
    (tl, tr, br, bl) = rect
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warpped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warpped

def preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image,7)
    #cv2.imshow("gray_blur", image)
    ret,image = cv2.threshold(image,80 ,255,cv2.THRESH_BINARY_INV)
    return image

def process(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    epsilon = 0.01*cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, epsilon, True)
    return contours, approx

