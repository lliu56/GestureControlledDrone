import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import math
# camera
cap = cv2.VideoCapture(0)

##initialize
detector = htm.handDetector()




while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #results = hands.process(imgRGB)
    detector.findHands(img)
    lmList = detector.findPosition(img)

    ###Finger Postion###
    #initialize
    fingerPosList = {'Index_Up':False,'Index_Down':False,'Index_Left':False, 'Index_Right':False,
                     'Middle_Up':False,'Middle_Down':False,'Middle_Left':False,
                     'Middle_Right': False,
                     'Thumb_Ring_Dis':False,'Thumb_Pinky_Dis':False }
    ###check which finger is up or down###
    if len(lmList) != 0:
        ##index##
        if lmList [8][2]< lmList [7][2]-20:
            fingerPosList['Index_Up']= True
        elif lmList[5][2] > lmList[0][2]:
            fingerPosList['Index_Down'] = True
        elif lmList [8][1]< lmList [7][1]-20:
            fingerPosList['Index_Left']= True
        elif lmList [8][1]> lmList [7][1]+20:
            fingerPosList['Index_Right'] = True

        ##Middle##
        if lmList [12][2]< lmList [11][2]-20:
            fingerPosList['Middle_Up']= True
        elif lmList[9][2] > lmList[0][2]:
            fingerPosList['Middle_Down'] = True
        elif lmList [12][1]< lmList [11][1]-20:
            fingerPosList['Middle_Left']= True
        elif lmList [12][1]> lmList [11][1]+20:
            fingerPosList['Middle_Right'] = True

        ##Distances###
        if (math.hypot(lmList [4][1]- lmList [16][1],    # distance between thumb and ring
                      lmList [4][2]- lmList [16][2]))< 30:
            fingerPosList['Thumb_Ring_Dis'] = True
        elif (math.hypot(lmList[4][1] - lmList[20][1],  # distance between middle finger and index
                       lmList[4][2] - lmList[20][2])) < 30:
            fingerPosList['Thumb_Pinky_Dis'] = True

    print (fingerPosList)
    cv2.imshow('Ctl Window', img)
    cv2.waitKey(1)