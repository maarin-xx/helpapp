import numpy as np
import glob
#import matplotlib
import cv2
import time

class MakeImage:
    video=cv2.VideoCapture(0)
    cap=cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

    object_point = np.zeros((6 * 8, 3), np.float32)
    object_point[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    object_points = []
    object_points2 = []
    image_points_left = []
    image_points_right = []


    check, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]

    print(check)
    print(frame)

    cv2.imshow("Capturing", frame)

    cv2.waitKey(0)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    video.release()

    video1=cv2.VideoCapture(0)
    video2=cv2.VideoCapture(1)
    check1, frame1 = video1.read()
    check2, frame2 = video1.read()
    print(check1)
    print(frame1)
    path = '/OpenCV/Scripts/Images'
    cv2.imwrite(os.path.join(path , 'Left.jpg'), frame1)
    cv2.imwrite(os.path.join(path , 'Right.jpg'), frame2)
    cv2.imshow("Capturing", frame)
    cv2.waitKey(0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    video.release()
