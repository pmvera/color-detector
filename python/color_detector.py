import cv2
import numpy as np

cap = cv2.VideoCapture(0)

width = cap.get(3)  # float
height = cap.get(4)  # float
total_size = width * height

colours = {"Rojo": ([155,25,0], [179,255,255]),
           "Azul": ([100,200,50], [140,255,255]),
           #"Verde": ([50,255,40], [70,255,60])
           #"Amarillo": ([103, 86, 65], [145, 133, 128])
           }

boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    ([50, 31, 4], [100, 88, 50]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
]

while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Get HSV interval for mask
    #col = np.uint8([[[0, 0, 0]]])
    #hsv_col = cv2.cvtColor(col,cv2.COLOR_BGR2HSV)
    #print (hsv_col)

    for colour in colours:
        lower = np.array(colours[colour][0])
        upper = np.array(colours[colour][1])
    #lower = np.array([100,200,200])
    #upper = np.array([140,255,255])

        mask = cv2.inRange(hsv, lower, upper)

        #dilation = cv2.dilate(mask, np.ones((10, 10), np.uint8), iterations=1)
        # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        # cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
        n_white_pix = np.sum(mask == 255)

        #print(colour, n_white_pix)
        if n_white_pix > 10000:
            print(colour, n_white_pix)
            cv2.imshow('dilation', mask)
            cv2.imshow('res', res)

        cv2.imshow('frame', frame)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
