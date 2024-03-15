import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("D:\\download\\ballonthefloorclip.mov")
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

def display_rois(small_rectangles, frame, n):
    for i, (x, y, w, h) in enumerate(small_rectangles):
        class_ = "noon"
        roi = frame[y:y+h, x:x+w]
        mask = color_detect_red(roi)
        red_area = cv2.countNonZero(mask)
        total_area = w * h
        red_percentage = (red_area / total_area) * 100

        mask_blue = color_detect_blue(roi)
        blue_area = cv2.countNonZero(mask_blue)
        total_area = w * h
        blue_percentage = (blue_area / total_area) * 100


        # Display the ROI and the red area percentage
        cv2.imshow(f"roi{i+1}_{n}_{class_}", roi)
        print(f"ROI {i+1}_{n} Red Percentage: {red_percentage:.2f}%")
        print(f"ROI {i+1}_{n} Blue Percentage: {blue_percentage:.2f}%")



        # if red_percentage > 7:
        #     class_ = "Red"
        #     cv2.imshow(f"roi{i+1}_{n}_{class_}", roi)
        #     return "Red"
        # if blue_percentage > 7:
        #     class_ = "Blue"
        #     cv2.imshow(f"roi{i+1}_{n}_{class_}", roi)
    return "Not Red" "Not Blue"

while True:
    ret, frame = cap.read()
    H, W = frame.shape[:2]
    # print(H, W)
    # 1080 1920

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    # cv2.resize(frame,(height,width), interpolation=cv2.INTER_AREA)
    
    # 1
    # cv2.rectangle(frame,(430,400),(580,650),(255,0,0),2)
    # large_rectangle = (430, 200, 250, 525)
    # small_rectangles = split_rectangle_into_rois(large_rectangle)
    # display_rois(small_rectangles, frame, 1)

    # # 2
    # cv2.rectangle(frame,(680,400),(830,650),(0,255,0),2)
    # large_rectangle = (680, 200, 250, 525)
    # small_rectangles2 = split_rectangle_into_rois(large_rectangle)
    # display_rois(small_rectangles2, frame,2)

    # # 3
    # cv2.rectangle(frame,(980,400),(1130,650),(0,0,255),2)
    # large_rectangle = (980, 200, 250, 525)
    # small_rectangles3 = split_rectangle_into_rois(large_rectangle)
    # display_rois(small_rectangles3, frame,3)

    # 4

    cv2.rectangle(frame,(1280,400),(1430,650),(255,255,0),2)
    large_rectangle = (1280, 400, 150, 230)
    small_rectangles4 = split_rectangle_into_rois(large_rectangle)

    display_rois(small_rectangles4, frame,4)

    # #5
    # cv2.rectangle(frame,(1000,0),(1250,525),(0,255,255),2)
    # large_rectangle = (1000, 0, 250, 525)
    # small_rectangles5 = split_rectangle_into_rois(large_rectangle)
    # display_rois(small_rectangles5, frame)

    
    # 2 
        

    # Process the ROI as needed

    cv2.imshow("frame", frame)
    
    
cap.release()
cv2.destroyAllWindows()