import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def calculate_distance(center1, center2):
    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance

def color_detect_red(bgr):
    
    red_lower = np.array([0, 0, 100])
    red_upper = np.array([76, 54, 244]) 

    purple_lower = np.array([100, 0, 100])
    purple_upper = np.array([150, 90, 161])

    dist_to_red = np.linalg.norm(bgr - (red_lower + red_upper) / 2)
    dist_to_purple = np.linalg.norm(bgr - (purple_lower + purple_upper) / 2)

    if dist_to_red < dist_to_purple:
        return "Red"
    else:
        return "Purple"
    
def color_detect_blue(bgr):
    
    blue_lower = np.array([100, 0, 0])
    blue_upper = np.array([226, 127, 48])

    purple_lower = np.array([80, 0, 80])
    purple_upper = np.array([150, 90, 161])

    dist_to_blue = np.linalg.norm(bgr - (blue_lower + blue_upper) / 2)
    dist_to_purple = np.linalg.norm(bgr - (purple_lower + purple_upper) / 2)

    if dist_to_blue < dist_to_purple:
        return "Blue"
    else:
        return "Purple"

def draw_rectangle_Red(img, x, y, w, h, color):
    # cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
    # cx = (x + (x + w)) / 2
    # cy = (y + (y + h)) / 2
    bottomLeftCornerOfText = (x, y)

    position = (((x + (x + w)) / 2), ((y + (y + h)) / 2))
    text = "red Ball x, y" + str(position)
    cv2.putText(frame,"red" +text,bottomLeftCornerOfText,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
    # cv2.circle(frame, (frame.shape[1] //2, frame.shape[0] // 2),2, (255, 255, 255), 1)
    distance = calculate_distance(position, frame_center)
    return distance,position
    
    



def draw_rectangle_blue(img, x, y, w, h, color):
    cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)

    bottomLeftCornerOfText = (x, y)

    position = (((x + (x + w)) / 2), ((y + (y + h)) / 2))
    text = "Blue Ball x, y" + str(position)
    cv2.putText(frame,"Blue" +text,bottomLeftCornerOfText,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
    # cv2.circle(frame, (frame.shape[1] //2, frame.shape[0] // 2),2, (255, 255, 255), 1)
    distance = calculate_distance(position, frame_center)
    
    # distance_list.append(distance)
    # if distance ==  min(distance_list):
    #     cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)



def detect_circles(img):
    distance_list = []
    position_list = []
    
    count = 0
    text = ""
    # bottomLeftCornerOfText = (0, 0)
    
    # frame = cv2.imread(frame) # Read the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray)

    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=150,
        param1=50,
        param2=30,
        minRadius=125, # 50
        maxRadius=250 # 100
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        mask = np.zeros_like(gray)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        # distance_list = []
        # position_list = []
        for i in circles[0, :]:
            
            
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(mask, (i[0], i[1]), i[2], 255, thickness=cv2.FILLED)
            if 0 <= i[0] < frame.shape[1] and 0 <= i[1] < frame.shape[0]:
                center_pixel_color = frame[i[1], i[0]]
                class_color = color_detect_red(center_pixel_color) # color_detect_blue(center_pixel_color)
                print("RGB values at center of circle:", center_pixel_color, "Classified as:", class_color)
                if class_color == "Red": # "Blue"

                    count += 1
                    center = (i[0], i[1])
                    radius = i[2]
                    x, y = center[0] - radius, center[1] - radius
                    w, h = 2 * radius, 2 * radius
                    distance,position = draw_rectangle_Red(frame, x, y, w, h, (0, 0, 255))
                    draw_rectangle_Red(frame, x, y, w, h, (0, 0, 255))
                    
                    
                
                   
                    

                    
                    # text = "x,y" + str(bottomLeftCornerOfText)
                if class_color == "Blue": # "Blue"
                    count += 1
                    center = (i[0], i[1])
                    radius = i[2]
                    x, y = center[0] - radius, center[1] - radius
                    w, h = 2 * radius, 2 * radius
                    draw_rectangle_blue(frame, x, y, w, h, (0, 0, 255))

                    if distance_list!= []:
                        if distance ==  min(distance_list):
                            print("distance",distance),print("position",position)
                            index=distance_list.index(distance)
                            position = position_list[index]
                            pos = (int(position[0]), int(position[1]))
                                #for i in position:
                                #    pos.append(int(i))
                            print(f"pos : {pos}")
                            cv2.putText(frame,"near",pos,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                
                # if distance ==  min(distance_list):
                #     cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)
                    # bottomLeftCornerOfText = (x, y)
                    
                

                print(count)
                for i in range(0, count):
                    if distance not in distance_list:
                       
                        distance_list.aSppend(distance)
                        position_list.append(position)
                if distance_list!= []:
                        if distance ==  min(distance_list):
                            print("distance",distance),print("position",position)
                            index=distance_list.index(distance)
                            position = position_list[index]
                            pos = (int(position[0]), int(position[1]))
                                #for i in position:
                                #    pos.append(int(i))
                            print(f"pos : {pos}")
                            cv2.putText(frame,"near",pos,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                #print(distance_list)
                #print(position_list)
    
                        
                
            red_intensity = center_pixel_color[2]
                
            if red_intensity > 200:
                max_red_intensity = red_intensity
                try:
                    max_red_intensity_location = (i[0], i[1])
                except:
                    pass
                # center_max = (i[0], i[1])
                # radius_max= i[2]
                # x_max, y_max = center_max[0] - radius_max, center_max[1] - radius_max
                # w_max, h_max = 2 * radius_max, 2 * radius_max
                # draw_rectangle(frame, x_max, y_max, w_max, h_max, (255, 255, 255))
                
                
                        
        result = cv2.bitwise_and(frame, frame, mask=mask)
    

    # cv2.putText(frame, f"total ={count}", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 5)
    # print("Maximum red intensity:", max_red_intensity)
    # print("Coordinates of the maximum red intensity pixel:", max_red_intensity_location)

    
    # cv2.imshow('Result with Circles Masked', result)
    
    # cv2.imshow('detected circles', gray_blurred)
    # cv2.imshow('detected circles', mask)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return mask, count, text



# detect_circles('20231010_161302.jpg')
cap = cv2.VideoCapture(0)  
cap.set(cv2.CAP_PROP_EXPOSURE, 2) 
while True:
    ret, frame = cap.read() 
    if not ret:
        break
    # center of frame
    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
    cv2.circle(frame, (frame.shape[1] //2, frame.shape[0] // 2),2, (255, 255, 255), 1)

        
    # detect_circles(frame)
    mask, count, text = detect_circles(frame)

    cv2.putText(frame, f"total ={count}", (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 5)
    
    # cv2.putText(frame,"red" +text,bottomLeftCornerOfText,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow('frame circles', frame)
    cv2.imshow('detected circles', mask)


    # cv2.imshow('Circle Detection', result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
