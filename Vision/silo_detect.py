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


def color_detect_red(bgr):
    red_lower = np.array([0, 0, 100], np.uint8)
    red_upper = np.array([80, 80, 255], np.uint8)
    mask = cv2.inRange(bgr, red_lower, red_upper)

    return mask

def color_detect_blue(bgr):
    blue_lower = np.array([100, 0, 0], np.uint8)
    blue_upper = np.array([255, 153, 48], np.uint8)
    mask_blue = cv2.inRange(bgr, blue_lower, blue_upper)

    return mask_blue

def ColorInSilo(roi):
    # x = 38, y = 75
    state = ''
    rois = roi.copy()
    mask = color_detect_blue(roi)
    cv2.circle(rois,(45,30),1,(0,0,255),3)
    cv2.circle(rois,(65,20),1,(0,0,255),3)
    cv2.circle(rois,(85,20),1,(0,0,255),3)
    cv2.circle(rois,(105,30),1,(0,0,255),3)

    cv2.circle(rois,(45,46),1,(0,0,255),3)
    cv2.circle(rois,(65,56),1,(0,0,255),3)
    cv2.circle(rois,(85,56),1,(0,0,255),3)
    cv2.circle(rois,(105,46),1,(0,0,255),3)
    #rois[y,x]
    #rois[75,46]
    #cv2.putText(rois,f"RGB :{rois[46,45]}",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)
    
    mask_red = color_detect_red(roi)
    red_area = cv2.countNonZero(mask_red)
    mask_blue = color_detect_blue(roi)
    blue_area = cv2.countNonZero(mask_blue)

    red_point = [np.max(mask_red[46,45]), np.max(mask_red[56,65]), np.max(mask_red[56,85]), np.max(mask_red[46,105]), np.max(mask_red[30,45]),
           np.max(mask_red[20,65]), np.max(mask_red[20,85]), np.max(mask_red[30,105])]
    blue_point = [np.max(mask_blue[46,45]), np.max(mask_blue[56,65]), np.max(mask_blue[56,85]), np.max(mask_blue[46,105]), np.max(mask_blue[30,45]),
           np.max(mask_blue[20,65]), np.max(mask_blue[20,85]), np.max(mask_blue[30,105])]
    if red_point.count(255) > 5:
        cv2.putText(rois,f"Red",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)
        state = 'Red'
    elif blue_point.count(255) > 5:
        cv2.putText(rois,f"Blue",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)
        state = 'Blue'
    else:
        cv2.putText(rois,f"Empty",(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0),1)
        state = 'Empty'
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
        mask = color_detect_red(roi)
        red_area = cv2.countNonZero(mask)
        total_area = w * h
        red_percentage = (red_area / total_area) * 100

        mask_blue = color_detect_blue(roi)
        blue_area = cv2.countNonZero(mask_blue)
        total_area = w * h
        blue_percentage = (blue_area / total_area) * 100
        silo_state.append(rois[1])

        # Display the ROI and the red area percentage
        #cv2.imshow("point",ColorInSilo(roi))
        cv2.imshow(f"roi{i+1}_{n}_{class_}", roi)
        cv2.imshow(f"point{i}", rois[0])
        # print(f"ROI {i+1}_{n} Red Percentage: {red_percentage:.2f}%")
        # print(f"ROI {i+1}_{n} Blue Percentage: {blue_percentage:.2f}%")

    return silo_state


cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture("D:\\download\\ballonthefloorclip.mov")
while (True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(1920,1080))
    # print(frame.shape)
    H, W = frame.shape[:2]
    # print(H, W)
    # 1080 1920

    cv2.rectangle(frame,(1280,400),(1430,650),(255,255,0),2)
    large_rectangle = (1280, 400, 150, 230)
    small_rectangles4 = split_rectangle_into_rois(large_rectangle)

    print(display_rois(small_rectangles4, frame,4))

    Bin = ColorInSilo(frame)
    # cv2.imshow("Bin", Bin)
    # cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    
cap.release()
cv2.destroyAllWindows()