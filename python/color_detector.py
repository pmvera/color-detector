import cv2
import numpy as np

cap = cv2.VideoCapture(0)

width = cap.get(3)  # float
height = cap.get(4)  # float
total_size = width * height

colours = {"Rojo": ([125,100,0], [179,255,255]),
           "Azul": ([100,200,50], [140,255,255]),
           "Verde": ([65,55,90], [90,255,255])
           #"Amarillo": ([103, 86, 65], [145, 133, 128])
           }
while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Get HSV interval for mask
    #col_min = np.uint8([[[0, 0, 70]]])
    #col_max = np.uint8([[[170, 100, 255]]])
    #hsv_col_min = cv2.cvtColor(col_min,cv2.COLOR_BGR2HSV)
    #hsv_col_max = cv2.cvtColor(col_max,cv2.COLOR_BGR2HSV)
    #print (hsv_col_min, hsv_col_max)

    #lower = np.array([125,100,0])
    #upper = np.array([179,255,255])

    for colour in colours:
        lower = np.array(colours[colour][0])
        upper = np.array(colours[colour][1])

        mask = cv2.inRange(hsv, lower, upper)
        img_dilated = cv2.dilate(mask, np.ones((8,8), np.uint8), iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=img_dilated)

        contours, hierarchy = cv2.findContours(img_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        n_white_pix = np.sum(mask == 255)

        #print(colour, n_white_pix)
        if n_white_pix > 10000:
            print("Red", n_white_pix)

        cv2.imshow('mask', mask)
        cv2.imshow('morph', img_dilated)
        cv2.imshow('res', res)
        cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
