import cv2 as cv
import mediapipe as mp,numpy as np
import time,cv2,math
import handmod as hm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
wCam,hCam = 640 ,480
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = hm.handDetector(detectionCon=0.7)
sets = True

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
vol = 0
volbar = 0
volper = 0
minVol = volRange[0]
maxVol = volRange[1]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist,bbox = detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        x3,y3 = lmlist[20][1],lmlist[20][2]
        x4,y4 = lmlist[15][1],lmlist[15][2]
        x5,y5 = lmlist[16][1],lmlist[16][2]
        x6,y6 = lmlist[11][1],lmlist[11][2]
        if abs(x3-x4)<20 and abs(y3-y4)<20:
            volume.SetMasterVolumeLevel(vol, None)
            sets = False
            print(sets)
            cv.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv.FILLED)
            cv.putText(img, str(int(volper)), (20, 120), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
        if abs(x5-x6)<20 and abs(y5-y6)<20:
            sets = True
            print(sets)
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv.circle(img,(cx,cy),15,(255,0,255),cv.FILLED)
        cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),15,(255,0,255),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        length= math.hypot(x2-x1,y2-y1)
        #HandRange 50 - 300
        #volumeRange -65 - 0
        
        volbar = np.interp(length,[50,190],[400,150])
        volper = np.interp(length,[50,190],[0,100])
        if sets == True:
            vol = np.interp(length,[50,190],[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            volbar = np.interp(length,[50,190],[400,150])
            volper = np.interp(length,[50,190],[0,100])
            cv.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv.FILLED)
            
        if volper < 10:
            cv.circle(img,(cx,cy),15,(0,255,0),cv.FILLED)
        if volper > 90:
            cv.circle(img,(cx,cy),15,(255,0,0),cv.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv.imshow("Image", img)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
cv.destroyAllWindows()