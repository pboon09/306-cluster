import cv2 
import numpy as np
cap = cv2.VideoCapture("E:\coding\computervision\ABU\WIN_20231206_13_41_02_Pro.mp4") # Green

def horizontal(x_pos,binrary_image):
    apos = 999
    # Extract a single row from the binary image
    binary_image = binrary_image[x_pos:x_pos+1, :]
    binary_image_index = np.where(np.array(binary_image[0]) == 0)
    height, width = binrary_image.shape
    # Extract 8 sections from the binary image using NumPy
    section_width = width // 8
    binary_image_8bit = []

    for i in range(8):
        section = binary_image[:, i * section_width:(i + 1) * section_width]
        binary_value = 1 if np.any(section == 0) else  0
        binary_image_8bit.append(binary_value)

    # Calculate the average position of white pixels in the row
    if len(binary_image_index[0]) > 0:
        apos = np.average(binary_image_index[0])

    return np.array2string(np.round(apos).astype(np.int32),separator='') +':'+ ''.join(map(str, binary_image_8bit))
while (cap.isOpened()):
    check , frame = cap.read() 
    height, width, _ = frame.shape
    frames = cv2.resize(frame,(300,300))
    frame = cv2.GaussianBlur(frames,(23,23),cv2.BORDER_DEFAULT)
    frame = cv2.cvtColor(frame , cv2.COLOR_RGB2HSV)

    if check == True :
        x1 = 100
        x2 = 200
        y1 = 100
        y2 = 200
        camline = {
            "x1": 80,
            "x2": 360,
            "y1": 160,
            "y2": 480
        }
        h, s, v = cv2.split(frame)
        thresh,th1 = cv2.threshold(s,80,255,cv2.THRESH_BINARY_INV)
        showLine = th1.copy()
        # Draw line
        cv2.line(showLine, (0, x1), (width, x1), (255, 255, 255), 1)
        cv2.line(showLine, (0, x2), (width, x2), (255, 255, 255), 1)
        cv2.line(showLine, (y1, 0), (y1, height), (255, 255, 255), 1)
        cv2.line(showLine, (y2, 0), (y2, height), (255, 255, 255), 1)

        # Label line
        cv2.putText(
            frame,
            "line1",
            (100,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "line2",
            (100,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "line3",
            (200,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "line4",
            (200,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
            # kernel = np.ones((8,8),np.uint8)

        # th1 = cv2.erode(th1,kernel,iterations=2)
        # th1 = cv2.morphologyEx(th1,cv2.MORPH_OPEN,kernel,iterations=4)

        cv2.imshow("original",frames)
        cv2.imshow("hsv",frame)
        cv2.imshow("s",s)
        cv2.imshow("bi",showLine)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    else :
        break

cap.release()
cv2.destroyAllWindows()