from djitellopy import tello
from time import sleep
import GestureRecognitionModule as grm
import cv2
import time


#me = tello.Tello ()
#me.connect ()
#print (me.get_battery())

global pTime, cTime
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = grm.handDetector()
gDetector = grm.gestureDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)  # calling the findPosition fxn
    gestureList = gDetector.gestureId(lmList)
    #print (gestureList)

    #### drome movemetns 
    if gestureList ['Index_Up']: print (





    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (225, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)



