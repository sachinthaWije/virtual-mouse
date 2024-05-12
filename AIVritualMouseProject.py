import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

########################
wCam, hCam = 640, 480
smoothening = 3
frameReduction = 100
########################

pTime = 0
pLocationX, pLocationY = 0, 0
cLocationX, cLocationY = 0, 0

wScr, hScr = autopy.screen.size()
# print(wScr,hScr)

cap = cv2.VideoCapture(2)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(max_num_hands=2)
click_drag_mode = False
drag_start_point = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # index finger
        x2, y2 = lmList[12][1:]  # middle finger
        x4, y4 = lmList[16][1:]
        # print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
        # print(fingers)

        cv2.rectangle(img, (frameReduction, frameReduction), (wCam - frameReduction, hCam - frameReduction),
                      (255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameReduction, wCam - frameReduction), (0, wScr))
            y3 = np.interp(y1, (frameReduction, hCam - frameReduction), (0, hScr))

            cLocationX = pLocationX + (x3 - pLocationX) / smoothening
            cLocationY = pLocationY + (y3 - pLocationY) / smoothening

            autopy.mouse.move(cLocationX, cLocationY)
            cv2.circle(img, (x1, y1), 15, (255, 10, 200), cv2.FILLED)



            pLocationX,pLocationY=cLocationX,cLocationY


        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img, r=10)
            print(length)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 150, 50), cv2.FILLED)
                autopy.mouse.click()

        # if fingers[0] == 1 :
        #     x5 = np.interp(x4, (frameReduction, wCam - frameReduction), (0, wScr))
        #     y5 = np.interp(y4, (frameReduction, hCam - frameReduction), (0, hScr))
        #
        #     cLocationX1 = pLocationX + (x5 - pLocationX) / smoothening
        #     cLocationY1 = pLocationY + (y5 - pLocationY) / smoothening
        #
        #     cv2.circle(img, (x4, y4), 10, (100, 10, 200), cv2.FILLED)
        #     autopy.mouse.move(cLocationX1, cLocationY1)
        #     autopy.mouse.toggle(down=True)
            # if not click_drag_mode:cLocationY1
            #     click_drag_mode = True
            #     drag_start_point = (x1, y1)
            # else:
            #     click_drag_mode = False
            #     drag_end_point = (x1, y1)
            #     autopy.mouse.toggle(down=True)  # Press and hold mouse button
            #     autopy.mouse.smooth_move(drag_start_point[0], drag_start_point[1])
            #     autopy.mouse.smooth_move(drag_end_point[0], drag_end_point[1])
            #     autopy.mouse.toggle(down=False)  # Release mouse button



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
