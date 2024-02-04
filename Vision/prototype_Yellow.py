import cv2 
import numpy as np
#""C:\\Users\\User\\Pictures\\Camera Roll\\WIN_20240114_15_51_22_Pro.mp4""
cap = cv2.VideoCapture("E:\coding\computervision\ABU\WIN_20231206_13_41_43_Pro.mp4") # yellow
cap = cv2.VideoCapture("C:\\Users\\User\\Pictures\\Camera Roll\\WIN_20240114_16_20_05_Pro.mp4") # yellow
cap = cv2.VideoCapture("C:\\Users\\User\\Pictures\\Camera Roll\\WIN_20240114_16_30_55_Pro.mp4") # yellow
while (cap.isOpened()):
    check , frame = cap.read() 
    frames = cv2.resize(frame,(400,400))
    frame = cv2.GaussianBlur(frames,(23,23),cv2.BORDER_DEFAULT)
    frame = cv2.cvtColor(frame , cv2.COLOR_RGB2HSV)

    if check == True :
        x_line = [0,50,110,140,200,260,290,350,399]
        x = [35,65,125,185,215,275,335,365]
        y = 100
        h, s, v = cv2.split(frame)

        thresh,th1 = cv2.threshold(s,50,255,cv2.THRESH_BINARY_INV)

        cv2.imshow("original",frames)
        # cv2.imshow("Output",result)
        cv2.imshow("s",s)
        cv2.imshow("bi",th1)
        # print(len(th1),len(th1[0]))
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    else :
        break

cap.release()
cv2.destroyAllWindows()