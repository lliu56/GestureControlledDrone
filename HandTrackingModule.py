import cv2
import mediapipe as mp
import numpy as np
import time


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


############ dummy code to run hand tracking module#######################
def main():  ##### running all of the classes, attributes, and methods created in the main portion of the code
    global pTime, cTime
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)  # calling the findPosition fxn
        # because the fxn returns the lmList
        # so you assign the values of the method
        # to the list
        if len(lmList) != 0:  # check if there is actually any content in
            print (lmList)   # [(0,x,y),(1,x,y).....]
            # the list, if there is then print
            #print(lmList[4])  # print values for a certain landmark

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (225, 0, 0), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)
#############################################################################

if __name__ == '__main__':
    main()