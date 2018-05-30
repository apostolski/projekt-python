import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import math
def nothing(x):
    pass
start=time.time()
lefthand=[300,0];
timer=0
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")
fgbg = cv2.createBackgroundSubtractorMOG2()
counter=0
img_counter = 0
img=np.zeros((300,512,3),np.uint8)
cv2.createTrackbar('Ilosc punktow','test',1,500,nothing)
cv2.createTrackbar('Odleglosc pomiedzy punktami','test',1,255,nothing)
cv2.createTrackbar('Czulosc','test',2,10,nothing)
dystans=30
plt.show()
print("Rozpoczecie kalibracji")
while True:


    if (time.time()-start>6 and timer==0):
        print("koniec kalibracji")
        timer=1
        for i in corners:
            x,y = i.ravel()
            if x<lefthand[0]:
                lefthand=[x,y]
    ret, frame = cam.read()
    frame=cv2.flip(frame, 1 )
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    cv2.imshow("test", fgmask)
    punkty=cv2.getTrackbarPos('Ilosc punktow','test')
    silka=cv2.getTrackbarPos('Odleglosc pomiedzy punktami','test')
    czulkosc=cv2.getTrackbarPos('Czulosc','test')
    czulkosc=czulkosc/10
    corners = cv2.goodFeaturesToTrack(fgmask,punkty,czulkosc,silka)
    counter=counter%3
    ax=[]
    ay=[]
    odleglosc=30
    try:
        for i in corners:
            x,y = i.ravel()
            if (timer==1):
                temp=math.sqrt((lefthand[0]-x)**2+(lefthand[1]-y)**2)
                if (temp<50 and temp<odleglosc):
                   
                    odleglosc=temp
                    lefthand=[x,y]
            ax.append(x)
            ay.append(y)
        plt.plot(ax,ay,'*','r')
        plt.plot((600/2,lefthand[0]),(480/2,lefthand[1]))
        plt.axis([0,600,480,0])
        plt.draw()
        plt.pause(1e-17)
        plt.clf()
    except:
        pass
    
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
