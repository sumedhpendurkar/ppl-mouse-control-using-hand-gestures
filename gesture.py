"""
 ****************************************************************************
 * Mouse Control Using Hand Gestures
 *
 * Copyright (C)
 *  Sumedh Pendurkar <sumedh.pendurkar@gmail.com>
 *  Akash Patil <akashmpatil11@gmail.com>
 *  Tejas Nayak <tejasunayak@gmail.com>
 *  Varad Ghodake <varadghodake@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
 ******************************************************************************
"""

import cv2
import numpy as np
import math
from actions import *
from pymouse import PyMouse
import time
def dummy(x):
    pass
cap = cv2.VideoCapture(0)
count = 0
cv2.namedWindow("alltime") # create a window to be displayed
cv2.createTrackbar("Mouse Sensitivity", "alltime", 1, 200, dummy)
cv2.setTrackbarPos("Mouse Sensitivity", "alltime", 100)
ret, img = cap.read()
act = action(img.shape)
state = False
screen_x, screen_y = act.screen_size()
while(cap.isOpened()):
    time.sleep(0.05)
    ret, img = cap.read()

    #Unable to read msg.. retry opening webcam object
    if ret == False:
        print ("Error count %d", count)
        continue

    #Create a box where image recognization takes place
    img_x, img_y, _ = img.shape
    cv2.rectangle(img,(img_x,img_y),(00,00),(0,255,0),0)
    crop_img = img

    #Binarize
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)

    version = '2'
    (version, _, _) = cv2.__version__.split('.')

    #finding contours in the thresholded image
    if version is '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version is '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)
    
    #ask varad; Looks like it finds out maximum area contour
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
   
    #drawing a rectangle on crop_img
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    cv2.imshow("cropped and chopped", crop_img)

    #Finding convex hulls. and drawing it on black img
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    cv2.imshow("alltime", drawing)

    #find out hull and defects
    #defects stored in defects
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    thresh1 = cv2.drawContours(thresh1, contours[0], -1, (0,255,0), 3)
    cv2.imshow("drawing_cnt", thresh1)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.288
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    act.update_sensitivity(cv2.getTrackbarPos("Mouse Sensitivity", "alltime"))
    if count_defects == 1 and state:
        act.one(far)
        #mouse_cntrl.click(2,2,2)
    elif count_defects == 2 and state:
        act.two()
        #mouse_cntrl.click(2,2,1)
    elif count_defects == 3 and state:
        act.three()
        #mouse_cntrl.click(2,2,2)
    elif count_defects == 4 and state:
        act.four()
    else:
        act.zero()
    if not state:
        a = int(raw_input())
        if a == 1:
            state = True
    #cv2.imshow('drawing', drawing)
    #cv2.imshow('end', crop_img)
    #cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    #cv2.imshow('Contours', all_img)
    k = cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
