from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2
import motor

def white(arr):
    return arr[0] > arr[1] - 200

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
    image = cv2.medianBlur(image,5)
    ret,image = cv2.threshold(image,130 ,255,cv2.THRESH_BINARY_INV)
    return image

def process(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    epsilon = 0.01*cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, epsilon, True)
    return contours, approx

def main(): 
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (160, 120)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(160, 120))

    # allow the camera to warmup
    time.sleep(2)
     
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #motor.stop(0.2)
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image_original = frame.array
        pts = np.array([(32, 0), (135, 0), (159, 119), (0, 119)])
        image = fourPointTransform(image_original, pts)
        cv2.imshow("image", image)
        image = preprocess(image)

        #im = image_original.copy()
        
        #for pt in pts:
            #cv2.circle(im, tuple(pt), 2, (0, 255, 0), 2)
        #cv2.circle(im, (159, 119), 2, (0, 255, 0), 2)

        #cv2.imshow("image", im)

        #motor.switchOnLED()
        
        contours, approx = process(image.copy())
        approx = approx.reshape(-1, 1, 2)
        cv2.polylines(image_original, [approx], True, (0, 255, 0), 2)

        height, width = image.shape

        top, center, bottom = np.array_split(image, 3)

        block = [np.array_split(top, 3, axis=1), np.array_split(center, 3, axis=1), np.array_split(bottom, 3, axis=1)]

        count = [[np.array([(200 < block[0][0]).sum(), (200 > block[0][0]).sum()]),np.array([(200 < block[0][1]).sum(), (200 > block[0][1]).sum()]),np.array([(200 < block[0][2]).sum(), (200 > block[0][2]).sum()])], [np.array([(200 < block[1][0]).sum(), (200 > block[1][0]).sum()]), np.array([(200 < block[1][1]).sum(), (200 > block[1][1]).sum()]), np.array([(200 < block[1][2]).sum(), (200 > block[1][2]).sum()])], [np.array([(200 < block[2][0]).sum(), (200 > block[2][0]).sum()]), np.array([(200 < block[2][1]).sum(), (200 > block[2][1]).sum()]), np.array([(200 < block[2][2]).sum(), (200 > block[2][2]).sum()])]]

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
        cv2.imshow("processed image", image_original)
        '''
        for i in range(len(block)):
            for j in range(len(block[i])):
                cv2.imshow("a"+ str(i) + str(j), block[i][j])
        '''

        
        #cv2.imwrite(str(int(time.time()))+".jpg", image_original)

        #break

        key = cv2.waitKey(1) & 0xFF
     
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        #GPIO.cleanup()
        #break
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
