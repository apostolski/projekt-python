import numpy as np
import cv2
from matplotlib import pyplot as plt

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")

fgbg = cv2.createBackgroundSubtractorMOG2()
counter=0
img_counter = 0
plt.show()
while True:
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    cv2.imshow("test", fgmask)
    corners = cv2.goodFeaturesToTrack(fgmask,40,0.4,3)
    #corners = np.int0(corners)

    counter=counter%3
    ax=[]
    ay=[]
    for i in corners:
        x,y = i.ravel()
        ax.append(x)
        ay.append(y)
    plt.plot(ax,ay,'*','r')
    plt.axis([0,600,480,0])
    plt.draw()
    plt.pause(1e-17)
    plt.clf()

    
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
