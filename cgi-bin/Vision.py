"""
Overview: This module provides Vision based functionality
using the camera to execute different actions.

Packages:
    - pip install opencv-python cvzone pycaw comtypes
"""


import cv2
from cvzone.HandTrackingModule import HandDetector
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from cvzone.PoseModule import PoseDetector



# flask
def set_volume(volume_percent):
    """
    set_volume(): Set the system volume based on the volume_percent value.
    Parameters:
        - volume_percent: requires a int() value between 0 and 100 as a percentage.
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_percent / 100.0, None)



# flask
def ChangeVol_with_Hand():
    """
    Detect_hand(): This function detects the hand using the camera and uses the set_volume() function
    to change the volume based on the distance between index and thumb finger position.
    Parameters:
        -None
    Returns:
        -None
    """
    cap = cv2.VideoCapture(0)

    Detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    while True:

        sucess,frame = cap.read()

        hands, frame = Detector.findHands(frame, draw=True, flipType=True)

        if hands:
            hand1 = hands[0] 
            lmList1 = hand1["lmList"]  
            length, info, img = Detector.findDistance(lmList1[4][0:2], lmList1[8][0:2], frame, color=(255,0,0),scale=1)

            if length < 20:
                volume_percent = 0
            elif length > 100:
                volume_percent = 100
            else:
                volume_percent = int((length - 20) * (100 / 80))     
            set_volume(volume_percent)
        
        cv2.imshow('myframe',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


# flask
def finger_counter():
    """
    finger_counter(): Counts the number of fingers up on the screen using the cvzone libarary.
    Returns:
        - counter_initial: The number of fingers up on the screen after displaying the first hand.
        - counter_final: The number of fingers up on the screen after displaying more then one hand.
    """
    cap = cv2.VideoCapture(0)

    detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)


    while True:
        success, img = cap.read()

        hands, img = detector.findHands(img, draw=True, flipType=True)
        counter_final ,counter_initial= 0,0
        if hands:
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinqates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            fingers1 = detector.fingersUp(hand1)
            counter_initial = fingers1.count(1)
            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                bbox2 = hand2["bbox"]
                center2 = hand2['center']
                handType2 = hand2["type"]

                fingers2 = detector.fingersUp(hand2)
                counter_final= fingers2.count(1)

            
        print(" ")
        print(f'{counter_initial+counter_final}')
        counter = counter_initial+counter_final
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
    return counter



def TPose_detector():
    """
    Function to detect T-pose using a webcam video stream.
    """
    cap = cv2.VideoCapture(0)

    detector = PoseDetector(staticMode=False,
                            modelComplexity=1,
                            smoothLandmarks=True,
                            enableSegmentation=False,
                            smoothSegmentation=True,
                            detectionCon=0.5,
                            trackCon=0.5)

    while True:
        success, img = cap.read()

        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

        if lmList:
            center = bboxInfo["center"]

            # Draw a circle at the center of the bounding box
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

            length, img, info = detector.findDistance(lmList[11][0:2],
                                                    lmList[15][0:2],
                                                    img=img,
                                                    color=(255, 0, 0),
                                                    scale=10)
            angle1, img = detector.findAngle(lmList[12][0:2],
                                            lmList[11][0:2],
                                            lmList[15][0:2],
                                            img=img,
                                            color=(255, 0, 255),
                                            scale=5)
            
            angle2, img = detector.findAngle(lmList[11][0:2],
                                            lmList[12][0:2],
                                            lmList[16][0:2],
                                            color=(255, 0, 255),
                                            img=img,
                                            scale=5)
            
            
            rightisCloseAngle180 = detector.angleCheck(myAngle=angle1,
                                                targetAngle=180,
                                                offset=10)
            leftisCloseAngle180 = detector.angleCheck(myAngle=angle2,
                                                targetAngle=180,
                                                offset=10)
            
            if rightisCloseAngle180 and leftisCloseAngle180:
                cv2.putText(img,  
                    'T-pose',  
                    (50, 50),  
                    cv2.FONT_HERSHEY_SIMPLEX , 1,  
                    (0, 255, 255),  
                    2,  
                    cv2.LINE_4) 
    
        # Display the frame in a window
        cv2.imshow("Image", img)

        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cv2.destroyAllWindows()
    cap.release()
