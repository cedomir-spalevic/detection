from __future__ import print_function
import cv2 as cv
import sys

classifiers = {
    "--face": "classifiers/haarcascade_frontalface_alt.xml",
    "--eye": "classifiers/haarcascade_eye.xml"
}

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    # Detect all faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 0), 4)

        # In each face, detect eyes
        faceFrame = frame_gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(faceFrame)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2) * .25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

    cv.imshow('Capture - Detection Demo', frame)

# 1. Load the cascades
face_cascade = cv.CascadeClassifier()
eye_cascade = cv.CascadeClassifier()
face_cascade.load('classifiers/haarcascade_frontalface_alt.xml')
eye_cascade.load('classifiers/haarcascade_eye.xml')


# 2. Read the video stream
cap = cv.VideoCapture(0)
if not cap.isOpened:
    print('Error opening camera')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('Frame not captured')
        break

    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break