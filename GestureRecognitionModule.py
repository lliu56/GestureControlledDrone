import cv2
import mediapipe as mp
import numpy as np
import time
import math


gestureList = []
class handDetector():
    # initialization
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5,
                 trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # referencing to mediapipe library
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print (results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        #### creating a list of x and y coordinates
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])  # this will add the id,cx and cy to the lmList
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)
        return lmList  # returning landmark list whether its filled or nah

class gestureDetector():
    def __init__(self):
        self.detector = handDetector()

    def gestureId (self,list):

        fingerPosList = {'Index_Up': False, 'Index_Down': False, 'Index_Left': False, 'Index_Right': False,
                         'Middle_Up': False, 'Middle_Down': False, 'Middle_Left': False,
                         'Middle_Right': False,
                         'Thumb_Ring_Dis': False, 'Thumb_Pinky_Dis': False,'Pinky_Up':False,
                         'Thumb_RingKnuckle_Dis':False}
        ###check which finger is up or down###
        if len(list)!= 0:
            if list[8][2] < list[7][2] - 30:
                fingerPosList['Index_Up'] = True
            elif list[5][2] > list[0][2]:
                fingerPosList['Index_Down'] = True
            elif list[8][1] < list[7][1] - 30:
                fingerPosList['Index_Left'] = True
            elif list[8][1] > list[7][1] + 30:
                fingerPosList['Index_Right'] = True

            ##Middle##
            if list[12][2] < list[11][2] - 30:
                fingerPosList['Middle_Up'] = True
            elif list[9][2] > list[0][2]:
                fingerPosList['Middle_Down'] = True
            elif list[12][1] < list[11][1] - 30:
                fingerPosList['Middle_Left'] = True
            elif list[12][1] > list[11][1] + 30:
                fingerPosList['Middle_Right'] = True

            ##Distances###
            if (math.hypot(list[4][1] - list[16][1],  # distance between thumb and ring
                           list[4][2] - list[16][2])) < 25:
                fingerPosList['Thumb_Ring_Dis'] = True
            elif (math.hypot(list[4][1] - list[20][1],  # distance between middle finger and index
                             list[4][2] - list[20][2])) < 25:
                fingerPosList['Thumb_Pinky_Dis'] = True
            elif (math.hypot(list[4][1] - list[15][1],  # distance between middle finger and index
                             list[4][2] - list[15][2])) < 25:
                fingerPosList['Thumb_RingKnuckle_Dis'] = True

            #pinky
            if list[20][2] < list[19][2] -20:
                fingerPosList['Pinky_Up'] = True

        (fingerPosList)
        return fingerPosList




############ dummy code to run hand tracking module#######################
def main():  ##### running all of the classes, attributes, and methods created in the main portion of the code
    global pTime, cTime
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    gDetector = gestureDetector()

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)  # calling the findPosition fxn
        gestureList=gDetector.gestureId(lmList)
        print (gestureList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (225, 0, 0), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)
#############################################################################

if __name__ == '__main__':
    main()