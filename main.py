from utils import *
import time
import cv2
#import pandas as pd
#import numpy as np

'''
def select_api():
    df = pd.read_csv("/content/경기도_성남시_주정차금지(지정)구역_20220428_1651144031393_205491.csv", encoding='cp949')
    df.head(3)
'''

def start_drone(): #차 인식하기 위해 드론 띄우기.
    myDrone.takeoff()
    time.sleep(5)

def cardetect():
    # Create our body classifier
    car_classifier = cv2.CascadeClassifier('car.xml')

    myDrone.streamon()  # 동영상 촬영 시작
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)

    cap = cv2.frame_read

    while cap.isOpened():

        battary = myDrone.get_battery()  # battary가 30이하면 착륙
        if battary <= 30:
            myDrone.land()

        time.sleep(.05)
        # Read first frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Pass frame to our car classifier
        cars = car_classifier.detectMultiScale(gray, 1.4, 2)

        # Extract bounding boxes for any bodies identified
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.imshow('Cars', frame)

        if cv2.waitKey(1) == 13:  # is the Enter Key
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    myDrone = initTello() #초기 설정
    start_drone()
    cardetect()

        
