import cv2
import time
import handtrackingmodule as htm
import numpy as np
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def get_frames():

    overlayList=[]#list to store all the images

    brushThickness = 25
    # JUNHO:
    brushTest = 200

    eraserThickness = 70
    drawColor=(255,0,255)#setting purple color

    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)# defining canvas

    #images in header folder
    folderPath="Header"
    myList=os.listdir(folderPath)#getting all the images used in code
    #print(myList)
    for imPath in myList:#reading all the images from the folder
        image=cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)#inserting images one by one in the overlayList
    header=overlayList[0]#storing 1st image 
    cap=cv2.VideoCapture(0)

    # JUNHO: 3,4가 가로 세로 크기입니다.
    cap.set(3,1280)#width
    cap.set(4,720)#height

    detector = htm.handDetector(detectionCon=1, maxHands=1)#making object

    while True:

        # 1. Import image
        success, img = cap.read()

        # JUNHO:1이 좌우 반전이고, 다른 인수를 주면 또 달라질 수 있음.
        img=cv2.flip(img,1)#for neglecting mirror inversion
        
        # 2. Find Hand Landmarks
        img = detector.findHands(img)#using functions fo connecting landmarks
        lmList,bbox = detector.findPosition(img, draw=False)#using function to find specific landmark position,draw false means no circles on landmarks
        
        if len(lmList)!=0:
            #print(lmList)
            x1, y1 = lmList[8][1],lmList[8][2]# tip of index finger
            x2, y2 = lmList[12][1],lmList[12][2]# tip of middle finger
            
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            #print(fingers)

            # 4. If Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp,yp=0,0
                #print("Selection Mode")
                #checking for click
                if y1 < 125:
                    if 250 < x1 < 450:#if i m clicking at purple brush
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:#if i m clicking at blue brush
                        header = overlayList[1]
                        drawColor = (255, 100, 0)
                    elif 800 < x1 < 950:#if i m clicking at green brush
                        header = overlayList[2]
                        drawColor = (0,127,255)
                    elif 1050 < x1 < 1200:#if i m clicking at eraser
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)#selection mode is represented as rectangle


            # 5. If Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)#drawing mode is represented as circle
                #print("Drawing Mode")
                if xp == 0 and yp == 0:#initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                    xp, yp = x1, y1 # so to avoid that we set xp=x1 and yp=y1
                #till now we are creating our drawing but it gets removed as everytime our frames are updating so we have to define our canvas where we can draw and show also
                
                #eraser
                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                elif drawColor == (0,127,255):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushTest)#gonna draw lines from previous coodinates to new positions 
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushTest)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)#gonna draw lines from previous coodinates to new positions 
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp,yp=x1,y1 # giving values to xp,yp everytime 
            
            #merging two windows into one imgcanvas and img
        
        # 1 converting img to gray
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        
        # 2 converting into binary image and thn inverting
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)#on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask
        
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)#converting again to gray bcoz we have to add in a RGB image i.e img
        
        # (1)-------------------------------------
        img_shape = img.shape # img shape를 확인합니다.
        img_dtype = img.dtype # img type을 확인합니다.

        imgInv = cv2.resize(imgInv, (img_shape[1], img_shape[0])) # img와 같은 크기로 변경합니다.
        imgInv = imgInv.astype(img_dtype) # img와 같은 타입으로 변경합니다.
        # -------------------------------------

        #add original img with imgInv ,by doing this we get our drawing only in black color
        img = cv2.bitwise_and(img,imgInv)




        
        # (2)-------------------------------------
        img_shape = img.shape # img shape를 확인합니다.
        img_dtype = img.dtype # img type을 확인합니다.

        imgCanvas = cv2.resize(imgCanvas, (img_shape[1], img_shape[0])) # img와 같은 크기로 변경합니다.
        imgCanvas = imgCanvas.astype(img_dtype) # img와 같은 타입으로 변경합니다.
        # -------------------------------------

        #add img and imgcanvas,by doing this we get colors on img
        img = cv2.bitwise_or(img,imgCanvas)


        #setting the header image
        img[0:125,0:1280]=header# on our frame we are setting our JPG image acc to H,W of jpg images

        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)

        ret, frame = cv2.imencode('.jpg', img)
        frame = frame.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
