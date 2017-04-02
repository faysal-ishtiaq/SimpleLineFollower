import RPi.GPIO as GPIO
import time
import sys

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)


def switchOnLED():
    init()
    GPIO.output(18, GPIO.HIGH)


def stop(tf):
    init()

    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)

    time.sleep(tf)
    GPIO.cleanup()


def forward(tf):
    init()

    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)

    time.sleep(tf)
    GPIO.cleanup()



def backward(tf):

    init()

    GPIO.output(17, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)

    time.sleep(tf)
    GPIO.cleanup()

def right(tf):

    init()

    GPIO.output(17, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)

    time.sleep(tf)
    GPIO.cleanup()


def left(tf):

    init()

    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)

    time.sleep(tf)
    GPIO.cleanup()

    


