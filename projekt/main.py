import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import math
import string

def nothing(x):
    pass
def prosta1(x):
    return 1.14*x-244
def znajdz_rownanie(x,y):
    rownanie_prostej=[(y[0]-y[1])*(-1)/(x[1]-x[0]),(-y[0]*x[1]+y[1]*x[0])*(-1)/(x[1]-x[0])]
    return rownanie_prostej
def znajdz_prostopadla(rownanie,x,y):
    prostopadla_do_prostej=(-1)/rownanie[0]
    prostopadla_do_prostej=[prostopadla_do_prostej,x[0]*prostopadla_do_prostej*(-1)+y[0]]
    return prostopadla_do_prostej
class core_prosta:
    def __init__(self,x,y,dol):
        self.x=x
        self.y=y
        self.dol=dol
        self.rownanie=znajdz_rownanie(x,y)
        self.rownaniepp=znajdz_prostopadla(self.rownanie,x,y)
        self.prawo=((((y[0]-dol)-self.rownaniepp[1])/self.rownaniepp[0])-x[0])
        self.xplota=[x[0],x[1],x[1]+self.prawo,x[0]+self.prawo,x[0]]
        self.yplota=[y[0],y[1],y[1]-dol,y[0]-dol,y[0]]
def zplotuj(Obiekt):
        for x in Obiekt:
            plt.plot(x.xplota,x.yplota)
def sprawdzhitboxa(Klasa,x,y):
    for Obiekt in Klasa:
        odleglosc_x=Obiekt.x[1]-Obiekt.x[0]
        odleglosc_y=Obiekt.y[1]-Obiekt.y[0]
        dlugosc_krzywej_x=math.sqrt(odleglosc_x**2+odleglosc_y**2)
        dlugosc_krzywej_y=math.sqrt(Obiekt.dol**2+Obiekt.prawo**2)
        wspolczynniky=dlugosc_krzywej_y/odleglosc_y
        wspolczynnikx=dlugosc_krzywej_x/odleglosc_x
        boola=(y>(x*Obiekt.rownaniepp[0]+Obiekt.rownaniepp[1])and y<(x*Obiekt.rownanie[0]+Obiekt.rownanie[1])) and y>((x*Obiekt.rownanie[0]+Obiekt.rownanie[1])-(Obiekt.dol*wspolczynnikx)) and (y<(x*Obiekt.rownaniepp[0]+Obiekt.rownaniepp[1]+dlugosc_krzywej_x*Obiekt.rownaniepp[0]*(-1)))
        if (boola):
            return True
    return False

statusplota=1

timer=0
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
fgbg = cv2.createBackgroundSubtractorMOG2()
counter=0
img_counter = 0
dab=cv2.imread('download.png',1)
img=np.zeros((300,512,3),np.uint8)
cv2.createTrackbar('Ilosc punktow','test',100,500,nothing)
cv2.createTrackbar('Odleglosc pomiedzy punktami','test',10,255,nothing)
cv2.createTrackbar('Czulosc','test',3,10,nothing)
dystans=30
if statusplota==1:
    plt.show()
Figura=[[[272,554],[334,478],110],[[52,282],[426,464],490],[[19,104],[113,218],75]]
Hitboxy=[]
Figury=[]
procent='0%'
for x in Figura:
    Hitboxy.append(core_prosta(x[0],x[1],x[2]))
for x in Hitboxy:
    Figury.append(Hitboxy)
    
while True:
    dab = cv2.resize(dab, (640, 480)) 
    ########################################
    ret, frame = cam.read()
    frame=cv2.flip(frame, 1 )
    ########################################
    procent='Stopien pokrycia: '+procent
    dst = cv2.addWeighted(frame,0.7,dab,0.3,0)  #Łączenie obrazu i nakładki z kanałem alpha
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(dst,procent,(10,40), font, 1,(255,255,255),2,cv2.LINE_AA)
    # Display image

    
    
    cv2.imshow("test", dst)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    fgmask=cv2.flip(fgmask, 0 )
    punkty=cv2.getTrackbarPos('Ilosc punktow','test')
    silka=cv2.getTrackbarPos('Odleglosc pomiedzy punktami','test')
    czulkosc=cv2.getTrackbarPos('Czulosc','test')
    
    if czulkosc==-1 or czulkosc==0:
        #cam.release()
        #cv2.destroyAllWindows() #Jezeli okno zostalo zamkniete
        break
    
    czulkosc=czulkosc/10
    corners = cv2.goodFeaturesToTrack(fgmask,punkty,czulkosc,silka)
    counter=counter%3
    #####Operacje na obrazie, wyswietlanie#####
    
    ax=[]
    ay=[]
    dx=[]
    dy=[]           #resetowanie wartosci wyswietlanych na wizualizacji danych
    resztax=[]
    resztay=[]
    odleglosc=30
    
    try:    #dla 1-szej klatki trzeba zrobic wyjatek bo skrypt usuwania tla potrzebuje bufora
        for i in corners:
            x,y = i.ravel()
            ax.append(x)
            ay.append(y)
            if(sprawdzhitboxa(Figury[0],x,y)):
                dx.append(x)
                dy.append(y)
            else:
                resztax.append(x)
                resztay.append(y)
        procenty=(len(dx)*100/len(ax))
        procenty=('{0:.1f}'.format(procenty))
        procent=str(procenty)+'%'
        if statusplota==1:
            zplotuj(Figury[0])
            plt.plot(dx,dy,'*')
            plt.plot(resztax,resztay,'*')
            plt.axis([0,600,0,480])
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
    
cam.release()
cv2.destroyAllWindows()
