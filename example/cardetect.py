# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:25:51 2020
@author: gaurav sahani
"""

import cv2
import time

# Create our body classifier
car_classifier = cv2.CascadeClassifier('car.xml')

# Initiate video capture for video file
cap = cv2.VideoCapture('C:\\Users\\Free\\PycharmProjects\\cardetech\\4K Video of Highway Traffic! - YouTube - Chrome 2022-10-05 10-00-46.mp4')

# Loop once video is successfully loaded
while cap.isOpened():

    time.sleep(.05)
    # Read first frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Pass frame to our car classifier
    cars = car_classifier.detectMultiScale(gray, 1.4, 2)

    # Extract bounding boxes for any bodies identified
    for (x,y,w,h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.imshow('Cars', frame)

        if(w>150):
            if(h>150):
                print("big w:"+str(w)+"    h:"+str(h)+"\n")

    if cv2.waitKey(1)== 13: #is the Enter Key
        break

cap.release()
cv2.destroyAllWindows()

