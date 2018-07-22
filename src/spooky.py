import Imager
from PIL import Image as img
import cv2
import DnnRecognizer
import numpy
import tempfile
import os

# TODO: argument
headless=False

# TODO: make this an argument
out_dir='output'

# TODO: Make the number of runs an argument

# This is the requirement of the model for detection
# don't feel like scaling generated images
IMG_WIDTH = 300
IMG_HEIGHT = 300

#####################################3

def spookLoop(max):
    keepSpookin = True
    currentAttempts = 0
    totalSpooks = 0
    while keepSpookin:
        img = generatePotentialSpook()
        frame = extractFrame(img)
        if (checkSpook(frame)):
            totalSpooks+=1
            print("Attempt ", currentAttempts, " generated our ", totalSpooks, " spooky image!")
            saveSpook(frame)
        currentAttempts+=1
        print("Spooks checked: %d         \r"%currentAttempts)
        if (currentAttempts >= max and max > 0):
            keepSpookin = False
    return totalSpooks

# Build image to test
def generatePotentialSpook():
    imager = Imager.Imager(IMG_WIDTH, IMG_HEIGHT)
    return imager.generateOneRGB()

# extract a numpy array based version of the image
def extractFrame(img):
    return numpy.array(img)

# is this image spooky?
def checkSpook(spookyFrame):
    in_width = IMG_WIDTH
    in_height = IMG_HEIGHT
    mean = [104, 117, 123]
    conf_threshold = 0.7

    showSpook(spookyFrame)

    frame_height = spookyFrame.shape[0]
    frame_width = spookyFrame.shape[1]

    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(spookyFrame, 1.0, (in_width, in_height), mean, False, False)

    # Run a model
    net.setInput(blob)
    detections = net.forward()

    faces = list()

    # parse the results
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
            y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
            x_right_top = int(detections[0, 0, i, 5] * frame_width)
            y_right_top = int(detections[0, 0, i, 6] * frame_height)

            cv2.rectangle(spookyFrame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (0, 255, 0))
            label = "Spooky Ghost Confidence: %.4f" % confidence
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            cv2.rectangle(spookyFrame, (x_left_bottom, y_left_bottom - label_size[1]),
                                (x_left_bottom + label_size[0], y_left_bottom + base_line),
                                (255, 255, 255), cv2.FILLED)
            cv2.putText(spookyFrame, label, (x_left_bottom, y_left_bottom),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return False

# if we're not headless then let's show in a window
def showSpook(spookyFrame):
    if (headless):
        return
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.imshow(winName, spookyFrame)
    k = cv2.waitKey(1)
    if (k==27):
        sys.exit("I guess this is too spooky!")

# save this spooky image to a random name
def saveSpook(frame):
    tmp = tempfile.NamedTemporaryFile(suffix=".png", prefix="spooky_", dir=out_dir, delete=False)
    tmp.close()
    cv2.imwrite(tmp.name, frame)

#####################################3
winName = 'A spooky ghost!?'
net = cv2.dnn.readNetFromCaffe("../deps/model.proto",
                               "../deps/model.caffe")

if (not headless):
    cv2.startWindowThread()
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    
spookLoop(0)
