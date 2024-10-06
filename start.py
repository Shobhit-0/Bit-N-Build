from ultralytics import YOLO
import cv2
import math
import time
import cvzone
import pandas as pd
import _mysql_connector as sql
cn=sql.connect(user="root", password="admin", host="localhost", database="management")
cr=cn.cursor()
classnames={0: 'person',
 1: 'bicycle',
 2: 'car',
 3: 'motorcycle',
 4: 'airplane',
 5: 'bus',
 6: 'train',
 7: 'truck',
 8: 'boat',
 9: 'traffic light',
 10: 'fire hydrant',
 11: 'stop sign',
 12: 'parking meter',
 13: 'bench',
 14: 'bird',
 15: 'cat',
 16: 'dog',
 17: 'horse',
 18: 'sheep',
 19: 'cow',
 20: 'elephant',
 21: 'bear',
 22: 'zebra',
 23: 'giraffe',
 24: 'backpack',
 25: 'umbrella',
 26: 'handbag',
 27: 'tie',
 28: 'suitcase',
 29: 'plate',
 30: 'skis',
 31: 'snowboard',
 32: 'sports ball',
 33: 'kite',
 34: 'baseball bat',
 35: 'baseball glove',
 36: 'skateboard',
 37: 'surfboard',
 38: 'tennis racket',
 39: 'bottle',
 40: 'wine glass',
 41: 'cup',
 42: 'fork',
 43: 'knife',
 44: 'spoon',
 45: 'bowl',
 46: 'banana',
 47: 'apple',
 48: 'sandwich',
 49: 'orange',
 50: 'broccoli',
 51: 'carrot',
 52: 'hot dog',
 53: 'pizza',
 54: 'donut',
 55: 'cake',
 56: 'chair',
 57: 'couch',
 58: 'potted plant',
 59: 'bed',
 60: 'dining table',
 61: 'toilet',
 62: 'tv',
 63: 'laptop',
 64: 'mouse',
 65: 'remote',
 66: 'keyboard',
 67: 'cell phone',
 68: 'microwave',
 69: 'oven',
 70: 'toaster',
 71: 'sink',
 72: 'refrigerator',
 73: 'book',
 74: 'clock',
 75: 'vase',
 76: 'scissors',
 77: 'teddy bear',
 78: 'hair drier',
 79: 'toothbrush'}
cutlery={"spoon":0,"plate":0,"fork":0,"knife":0,"wineglass":0,"person":0}
wait_time=5
index=[0]*80
cap=cv2.VideoCapture(0) #instead of 0 enter url here, i.e. the url of the cctv footage
cr.execute("Create table utensils(utensil name varchar(30), amount int);")
cap.set(3,490)
cap.set(4,320)
model=YOLO("yolov8l.pt")
while True:
    success,img=cap.read()
    results=model(img,stream=True)
    for r in results:
        boxes=r.boxes
        for box in boxes:
            #bounding box
            x1,y1,x2,y2= box.xyxy[0]
            x1,y1,x2,y2= int(x1),int(y1),int(x2),int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
            w,h=x2-x1,y2-y1
            cvzone.cornerRect(img,(x1,y1,w,h))
            #confidence
            conf=math.ceil(box.conf[0]*100)/100
            cls=int(box.cls[0])
            cvzone.putTextRect(img,f'{classnames[cls]} {conf}',(max(0,x1),max(35,y1)),scale=1,thickness=1,offset=5)
            if classnames[cls] == 'spoon':
                cutlery["spoon"]+=1
            if classnames[cls] == 'fork':
                cutlery["fork"]+=1
            if classnames[cls] == 'plate':
                cutlery["plate"]+=1
            if classnames[cls] == 'knife':
                cutlery["knife"]+=1
            if classnames[cls] == 'wineglass':
                cutlery["wineglass"]+=1
            if classnames[cls] == 'person':
                cutlery["person"]+=1
            print(cutlery)
            #class
            
   
    cv2.imshow("webcam",img)

    time.sleep(wait_time)
    cutlery={"spoon":0,"plate":0,"fork":0,"knife":0,"wineglass":0,"person":0}
    if (cv2.waitKey(1)==ord('e')):
        break
cap.release()
pd.read_sql
cv2.destroyAllWindows()