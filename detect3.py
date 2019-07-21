from darkflow.net.build import TFNet
import cv2
import numpy as np
from scipy import stats
import time
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt

import math



options ={
    'model':'cfg/yolo.cfg',
    'load':'bin/yolov2.weights',
    'threshold':0.2,
    'gpu' : 0.6
}

tfnet= TFNet(options)


cap =cv2.VideoCapture(0)
colors = [tuple(255*np.random.rand(3)) for i in range(100)]

ret = True
fps_time = 0
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)


while(True):
    
    ret,frame = cap.read()
    result = tfnet.return_predict(frame)
    
    for color,result_2 in zip(colors,result):
            tl= (result_2['topleft']['x'],result_2['topleft']['y'])
            br=(result_2['bottomright']['x'],result_2['bottomright']['y'])
            label= result_2['label']
            

            if label == "person":
                cv2.rectangle(frame,tl,br,(255,0,0),3)
                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    cv2.imshow('frame',frame)

cv2.destroyAllWindows()
cap.release()