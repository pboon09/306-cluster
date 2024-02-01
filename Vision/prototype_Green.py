import cv2 
import numpy as np
cap = cv2.VideoCapture("E:\coding\computervision\ABU\WIN_20231206_13_41_02_Pro.mp4") # Green
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
        thresh,th1 = cv2.threshold(s,80,255,cv2.THRESH_BINARY_INV)
        # kernel = np.ones((8,8),np.uint8)

        # th1 = cv2.erode(th1,kernel,iterations=2)
        # th1 = cv2.morphologyEx(th1,cv2.MORPH_OPEN,kernel,iterations=4)

        cv2.imshow("original",frames)
        cv2.imshow("hsv",frame)
        cv2.imshow("s",s)
        cv2.imshow("bi",th1)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    else :
        break

cap.release()
cv2.destroyAllWindows()