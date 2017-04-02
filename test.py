from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2
import motor
import util

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
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image_org = frame.array
        pts = np.array([(32, 0), (135, 0), (159, 119), (0, 119)])
        image_org = util.fourPointTransform(image_org, pts)
        image = util.preprocess(image_org.copy())
        #cv2.imshow("preprocessed", image)
        height, width = image.shape

        top, center_upper, center_lower, bottom = np.array_split(image, 4)

        block = [np.array_split(top, 4, axis=1), np.array_split(center_upper, 4, axis=1), np.array_split(center_lower, 4, axis=1), np.array_split(bottom, 4, axis=1)]
        
        contours, approx = util.process(image.copy())
        approx = approx.reshape(-1, 1, 2)
        cv2.polylines(image_org, [approx], True, (0, 255, 0), 2)
        #cv2.imshow("image", image_org)
        
        print(image.shape)
        
        b = []
        count = []
        for i in range(len(block)):
            for j in range(len(block[i])):
                a = np.array([(200 < block[i][j]).sum(), (200 > block[i][j]).sum()])
                print(a[0], a[1], a[0]+a[1], block[i][j].shape)
                #print(float(a[0])/(a[0]+a[1]))
                b.append(float(a[0])/(a[0]+a[1]))
                count.append(b)

        whites = []
        for i in range(len(block)):
            for j in range(len(block[i])):
                print(count[i][j])
                if util.white(count[i][j]):
                    #whites.append([i, j])
                    cv2.imshow("a"+ str(i) + str(j), block[i][j])
                    #print(count[i][j])
                    #print(i, j)
                    #print(block[i][j].shape)

        #print(whites)
        
        cv2.imshow("processed image", image)

        #util.decide(count)

        '''
        for i in range(len(block)):
            for j in range(len(block[i])):
                cv2.imshow("a"+ str(i) + str(j), block[i][j])
        '''

        #for wh in whites:
        #    cv2.imshow("img_"+str(wh[0])+str(wh[1]), block[wh[0]][wh[1]])
        #    print(wh[0])
        #    print(wh[1])

        key = cv2.waitKey(1) & 0xFF
     
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        #break
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
