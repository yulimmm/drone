from utils import *
import numpy as np
import time
import cv2

def start_drone(): #차 인식하기 위해 드론 띄우기.
    myDrone.takeoff()
    time.sleep(2)
    myDrone.move_up(20) #x: 20-500
    time.sleep(2)

def stream_drone():
    myDrone.streamon()  # 동영상 촬영 시작
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)
    img = frame_read.frame
    cv2.imshow("drone", img)
    return(img)


def cardetect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Pass frame to our car classifier
    cars = car_classifier.detectMultiScale(gray, 1.4, 2)

    # Extract bounding boxes for any bodies identified
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.imshow('Cars', frame)

        if (w > 150):
            if (h > 150):
                print("big w:" + str(w) + "    h:" + str(h) + "\n")
                myDrone.move_forward(20)
                time.sleep(5)

                if (w > 600):
                    if (h > 600):
                        print("down w:" + str(w) + "    h:" + str(h) + "\n")
                        myDrone.move_down(30)
                        time.sleep(5)


    # img.release()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    myDrone = initTello() #초기 설정

    for i in range(3): #대충 세 번 반복해라.
        start_drone()  # 시작해서 드론 띄우기

        # Create our body classifier
        car_classifier = cv2.CascadeClassifier('car.xml')
        while True:
            battary = myDrone.get_battery()  # battary가 30이하면 착륙
            if battary <= 30:
                myDrone.land()
                break
            else:
                print("battary is ok\n")
                cardetect(stream_drone())  # 자동차 인식 -> 앞으로 가기 -> 특정 라밸링 크기 보다 커지면 조금 내려오기 -> 내려오면 끝내기
                # 번호판인식
                if cv2.waitKey(1) == 13:  # is the Enter Key
                    break

        img.release()
        cv2.destroyAllWindows()

