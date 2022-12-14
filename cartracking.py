"""
Movement Commands:

Written as:

me.send_rc_control(0, 0, 0, 0)
The RC Control Command is in the following Configuration:
Pitch ( Left & Right)
Pitch ( Forward & Backward)
Throttle ( Up & Down )
Yaw ( Rotation)

Note:
Values in 100 to -100
"""
# Face Tracking Success on May-1-2021
# ©2021
# Face Tracking Trial
# By Shreyas Sharma
# ©2021 - Coded on May-1 2021
# SS-Corp™ Tetravaal© Robotics
# Special Thanks to Shalaw for inspiring the new movement calculation algorithm

import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()
# Getting the drones battery
print(me.get_battery())


me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 25, 0)
time.sleep(2.2)
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0



def findCar(img):
    car_classifier = cv2.CascadeClassifier('car.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = car_classifier.detectMultiScale(imgGray, 1.4, 2)
    myCarListC = []
    myCarListArea = []

    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myCarListC.append([cx, cy])
        myCarListArea.append(area)

        command1 = x
        command2 = y
        command3 = w
        command4 = h

        if command1 > 0:
            print("Drone Movement: Right")
        else:
            print("Drone Movement: Left")
        if command2 > 0:
            print("Drone Movement: Forward")
        else:
            print("Drone Movement: Backward")
        if command3 > 0:
            print(" Drone Movement: Up")
        else:
            print("Drone Movement: Down")
        if command4 > 0:
            print("Drone Movement: Yaw Right")
        else:
            print("Drone Movement: Yaw Left")


    if len(myCarListArea) != 0:
        i = myCarListArea.index(max(myCarListArea))

        return img, [myCarListC[i], myCarListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackCar( info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    if x == 0:
        speed = 0
        error = 0
    #print(speed, fb)
    me.send_rc_control(0, fb, 0, speed)
    return error

#cap = cv2.VideoCapture(1)

while True:

    #_, img = cap.read()

    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findCar(img)
    pError = trackCar( info, w, pid, pError)
    #print(“Center”, info[0], “Area”, info[1])
    cv2.imshow("SS-Corp Tetravaal", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
