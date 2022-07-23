from djitellopy import tello
from time import sleep
import GestureRecognitionModule as grm
import cv2
import time
import KeyPressModule as kp


kp.init()
me = tello.Tello ()
me.connect ()
print (me.get_battery())


detector = grm.handDetector()
gDetector = grm.gestureDetector()
class getGesture ():

    def __init__(self):
        self.detector = grm.handDetector()
        self.gDetector = grm.gestureDetector()

    def getGestureInput (self,list):
        displayText = ' '
        lr, fb, ud, yv = 0, 0, 0, 0
        fspeed = 25
        aspeed = 50
        global img
        # Backflip
        if list['Index_Up'] and list['Pinky_Up'] and list['Thumb_RingKnuckle_Dis']:
            me.flip('b')
            displayText ='Backflip'


        #fb/ud
        if   list['Index_Up'] and list['Middle_Up']:
            ud = fspeed
            displayText = 'Up'
        elif list['Index_Down'] and list['Middle_Down']:
            ud = -fspeed
            displayText = 'Down'
        elif list ['Index_Up']:
            fb = fspeed
            displayText = 'Forward'
        elif list ['Index_Down']:
            fb = -fspeed
            displayText = 'Backward'


        #lr roll/yaw
        if list['Index_Right'] and list['Middle_Right']:
            yv = aspeed
            displayText = 'Right Turn'
        elif list['Index_Left'] and list['Middle_Left']:
            yv = -aspeed
            displayText = 'Left Turn'
        elif list ['Index_Right']:
            lr = fspeed
            displayText = 'Right'
        elif list ['Index_Left']:
            lr = -fspeed
            displayText = 'Left'


       # take off and landing
        if list['Thumb_Ring_Dis'] :
            me.takeoff()
            displayText = 'Take-off'
        elif list['Thumb_Pinky_Dis']:
            me.land ()
            displayText = 'Land'
        if kp.getKey('l'):
            me.land ()
            displayText = 'Land'

        return [lr,fb,ud,yv,displayText]


def main():  ##### running all of the classes, attributes, and methods created in the main portion of the code
    global pTime, cTime
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    #me.RESOLUTION_480P()

    cap.set(3, 480)
    cap.set(4,720 )

    #sleep (0.1)
    detector = grm.handDetector()
    gDetector = grm.gestureDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)  # calling the findPosition fxn
        gestureList=gDetector.gestureId(lmList)
        #print (gestureList)
        ###fps###
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (225, 0, 0), 3)


        vals = getGesture()
        vals = vals.getGestureInput(gestureList)
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])  # indexing value
        cv2.putText(img, vals[4], (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0, 255), 3)
        sleep(0.1)
        print (vals)
        cv2.imshow('Image', img)
        cv2.waitKey(1)
    #############################################################################

if __name__ == '__main__':
    main()