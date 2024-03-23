import cv2
import numpy as np
import imutils

# image = cv2.imread('IMG_8401.jpg')


# height, width = 500, 500
# imgResize = cv2.resize(image,(height,width), interpolation=cv2.INTER_AREA)


def split_rectangle_into_rois(large_rect):
    x, y, width, height = large_rect
    small_height = height // 3 

    rect1 = (x, y, width, small_height)
    rect2 = (x, y + small_height, width, small_height)
    rect3 = (x, y + 2 * small_height, width, small_height)

    return [rect1, rect2, rect3]

def trackbar(roi, original_img, WindowName):
   #ดึงค่าจาก Trackber
    Lowblue   = cv2.getTrackbarPos("LB", WindowName)
    Lowgreen  = cv2.getTrackbarPos("LG", WindowName)
    Lowred    = cv2.getTrackbarPos("LR", WindowName)
    Highblue  = cv2.getTrackbarPos("HB", WindowName)
    Highgreen = cv2.getTrackbarPos("HG", WindowName)
    Highred   = cv2.getTrackbarPos("HR", WindowName)

    L = [Lowblue, Lowgreen, Lowred]
    H = [Highblue, Highgreen, Highred]
    
    # print(L)
    lower = np.array(L, np.uint8)
    upper = np.array(H, np.uint8)
    
    mask = cv2.inRange(roi, lower, upper)
    masked_img  = cv2.bitwise_and(original_img, original_img, mask=mask)
    masked_img = cv2.resize(masked_img,(800, 800))
    
    cv2.imshow(WindowName,masked_img )
    # cv2.imshow("Original Image", original_img)
    return mask

# def color_detect_red(bgr):
#     # red_lower = np.array([0, 0, 100], np.uint8)
#     # red_upper = np.array([80, 80, 255], np.uint8)
#     L, H = trackbar(frame, ori, "Red Trackbar")
#     red_lower = np.array([0, 0, 60], np.uint8)
#     red_upper = np.array([255, 70, 116], np.uint8)
#     mask = cv2.inRange(bgr, red_lower, red_upper)

#     return mask

# def color_detect_blue(bgr):
#     # blue_lower = np.array([100, 0, 0], np.uint8)
#     # blue_upper = np.array([255, 153, 48], np.uint8)
#     blue_lower = np.array([75, 36, 12], np.uint8)
#     blue_upper = np.array([145, 255, 85], np.uint8)
#     mask_blue = cv2.inRange(bgr, blue_lower, blue_upper)

#     return mask_blue

def ColorInSilo(roi):
    # x = 38, y = 75
    state = ''
    axis = [35, 68,
            32, 72,
            32, 78,
            35, 82,
            41, 68,
            44, 72,
            44, 78,
            41, 82]
    
    red = roi.copy()
    blue = roi.copy()
    rois = roi.copy()
    
    mask_red = trackbar(red, roi, "Red Trackbar")
    mask_blue = trackbar(blue, roi, "Blue Trackbar")

    red_point = [np.max(mask_red[axis[0],axis[1]]),     np.max(mask_red[axis[2],axis[3]]), 
                 np.max(mask_red[axis[4],axis[5]]),     np.max(mask_red[axis[6],axis[7]]), 
                 np.max(mask_red[axis[8],axis[9]]),     np.max(mask_red[axis[10],axis[11]]), 
                 np.max(mask_red[axis[12],axis[13]]),   np.max(mask_red[axis[14],axis[15]])]
    
    blue_point = [np.max(mask_blue[axis[0],axis[1]]),   np.max(mask_blue[axis[2],axis[3]]),
                  np.max(mask_blue[axis[4],axis[5]]),   np.max(mask_blue[axis[6],axis[7]]),
                  np.max(mask_blue[axis[8],axis[9]]),   np.max(mask_blue[axis[10],axis[11]]), 
                  np.max(mask_blue[axis[12],axis[13]]), np.max(mask_blue[axis[14],axis[15]])]
    
    if red_point.count(255) > 5:
        cv2.putText(rois,f"Red",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),1)
        state = 'Red'
    elif blue_point.count(255) > 5:
        cv2.putText(rois,f"Blue",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),1)
        state = 'Blue'
    else:
        cv2.putText(rois,f"Empty",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,255,255),1)
        state = 'Empty'

    cv2.circle(rois,(68,35),1,(0,255,0),1)
    cv2.circle(rois,(72,32),1,(0,255,0),1)
    cv2.circle(rois,(78,32),1,(0,255,0),1)
    cv2.circle(rois,(82,35),1,(0,255,0),1)

    cv2.circle(rois,(68,41),1,(0,255,0),1)
    cv2.circle(rois,(72,44),1,(0,255,0),1)
    cv2.circle(rois,(78,44),1,(0,255,0),1)
    cv2.circle(rois,(82,41),1,(0,255,0),1)
    # roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    # h, s, v = cv2.split(roi)
    # thresh,th1 = cv2.threshold(roi,80,255,cv2.THRESH_BINARY)
    # b,g,r = cv2.split(th1)
    # kernel = np.ones((2,2),np.uint8)
    # dilation = cv2.dilate(th1,kernel,iterations=5)
    # dilation = cv2.cvtColor(dilation,cv2.COLOR_BGR2GRAY)
    # thresh,th2 = cv2.threshold(dilation,200,255,cv2.THRESH_BINARY)
    # w = roi.shape[0]
    # h = roi.shape[1]
    return [rois, state]

def display_rois(small_rectangles, frame, n):
    silo_state = []
    for i, (x, y, w, h) in enumerate(small_rectangles):
        class_ = "noon"
        roi = frame[y:y+h, x:x+w]
        rois = ColorInSilo(roi)
        # mask_red = color_detect_red(roi)
        # red_area = cv2.countNonZero(mask_red)
        # total_area = w * h
        # red_percentage = (red_area / total_area) * 100

        # mask_blue = color_detect_blue(roi)
        # blue_area = cv2.countNonZero(mask_blue)
        # total_area = w * h
        # blue_percentage = (blue_area / total_area) * 100
        silo_state.append(rois[1])

        # Display the ROI and the red area percentage
        #cv2.imshow("point",ColorInSilo(roi))
        cv2.imshow(f"roi{i+1}_{n}_{class_}", rois[0])
        # cv2.imshow(f"point{i}", rois[0])
        # print(f"ROI {i+1}_{n} Red Percentage: {red_percentage:.2f}%")
        # print(f"ROI {i+1}_{n} Blue Percentage: {blue_percentage:.2f}%")

    return silo_state


cap = cv2.VideoCapture("D:\\download\\ballonthefloorclip.mov")
cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("C:\\Users\\User\\Pictures\\Camera Roll\\WIN_20240315_17_52_40_Pro.mp4")

cv2.namedWindow("Red Trackbar")
cv2.namedWindow("Blue Trackbar")

def display(value):
    pass

#เริ่มต้นสร้าง Tracker
# Default = [R, G, B]

# Red
# Low Red Default
LRD = [60, 0, 25]
# High Red Default
HRD = [112, 70, 255]

## Blue
# Low Blue Default
LBD = [12, 36, 75]
# High Blue Default
HBD = [85, 255, 145]
cv2.createTrackbar("LR","Red Trackbar",LRD[0],255,display)
cv2.createTrackbar("LG","Red Trackbar",LRD[1],255,display)
cv2.createTrackbar("LB","Red Trackbar",LRD[2],255,display)
cv2.createTrackbar("HR","Red Trackbar",HRD[0],255,display)
cv2.createTrackbar("HG","Red Trackbar",HRD[1],255,display)
cv2.createTrackbar("HB","Red Trackbar",HRD[2],255,display)

cv2.createTrackbar("LR","Blue Trackbar",LBD[0],255,display)
cv2.createTrackbar("LG","Blue Trackbar",LBD[1],255,display)
cv2.createTrackbar("LB","Blue Trackbar",LBD[2],255,display)
cv2.createTrackbar("HR","Blue Trackbar",HBD[0],255,display)
cv2.createTrackbar("HG","Blue Trackbar",HBD[1],255,display)
cv2.createTrackbar("HB","Blue Trackbar",HBD[2],255,display)

while (True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(1920,1080))
    ori = frame.copy()
    red = frame.copy()
    blue = frame.copy()
    H, W = frame.shape[:2]
    # print(H, W)
    # 1080 1920
    x = 1260
    w = 150
    y = 530
    h = 250
    # cv2.rectangle(frame,(1280,400),(1430,650),(255,255,0),2)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
    large_rectangle = (x, y, 150, 230)
    small_rectangles4 = split_rectangle_into_rois(large_rectangle)

    print(display_rois(small_rectangles4, frame,4))

    Bin = ColorInSilo(frame)
    # frame = color_detect_red(frame)
    # cv2.imshow("Bin", Bin)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    #print(frame.shape)
    
    
cap.release()
cv2.destroyAllWindows()