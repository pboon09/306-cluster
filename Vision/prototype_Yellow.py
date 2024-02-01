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

        # imgray_array = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    
        # max_value = 255        
        # _, th1 = cv2.threshold(imgray_array, 95, max_value, cv2.THRESH_BINARY)

        # th1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 255, 0)
        # th1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 0)
        thresh,th1 = cv2.threshold(s,50,255,cv2.THRESH_BINARY_INV)
        # thresh,th1 = cv2.threshold(s,10,255,cv2.THRESH_OTSU)
        # lower = np.array([0,0,0])
        # upper = np.array([0,255,255])
        # mask=cv2.inRange(th1,lower,upper)
        # result = cv2.bitwise_and(frame,frame,mask=mask)
        # gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
        # thresh,th2 = cv2.threshold(gray,75,255,cv2.THRESH_BINARY)
        # kernel = np.ones((8,8),np.uint8)

        # th1 = cv2.erode(th1,kernel,iterations=2)
        # th1 = cv2.morphologyEx(th1,cv2.MORPH_OPEN,kernel,iterations=4)

        # dot1 = (th1[y][x[0]]+th1[y][x[0]])
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