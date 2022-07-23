import cv2
import mediapipe as mp
import numpy as np
import time

#run video through webcam
cap = cv2.VideoCapture(0)

#Initializations
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands ()



while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)


    # drawing handlms

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        for id, lm in enumerate(handLms.landmark):
            ih, iw, ic = img.shape
            x, y = int(lm.x * iw), int(lm.y * ih)

    cv2.imshow('Ctl Window', img)
    cv2.waitKey(1)