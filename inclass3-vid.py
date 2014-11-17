#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb, Christian Gibbons, Michael Reyes
# In Class Assignment 3
# 11/18/14

# this code uses robot-view-ctrl.py as the base

# ******************************************************

import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import operator
import controller_include as ci


err = ci.CONTROLLER_REF()

# CV setup 
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

newx = 320
newy = 240

nx = 640
ny = 480

cx = nx/2
cy = ny/2

tracked = False

er = np.ones((3,3),np.uint8)
di = np.ones((2,2),np.uint8)

c = ach.Channel(ci.CONTROLLER_REF_NAME)
c.flush()

i=0
k = 0

while True:
    # Get Frame   
    vid = np.zeros((newx,newy,3), np.uint8) 
    ret, vid = cap.read()
    vid2 = cv2.resize(vid,(nx,ny))
    img = cv2.cvtColor(vid2,cv2.COLOR_BGR2HSV)
    # apply threshold to get only green pixels
    mask = cv2.inRange(img, np.array((60.,50.,50.)), np.array((85.,255.,255.)))
    erosion = cv2.erode(mask,er,iterations = 1)
    dilation = cv2.dilate(erosion,di,iterations = 1)
    m = cv2.moments(dilation)

    if(m['m00'] != 0.0):
	x = int(m['m10']/m['m00'])
	y = int(m['m01']/m['m00'])
	ex = -(cx - x)
	ey = cy - y
	err.x = ex
	err.y = ey
	c.put(err)
	print ex, ey
    else:
        print "!"

    if(m['m00'] != 0.0):
	cv2.circle(vid2, (x,y), 2, (0,0,255),-1) # small red circle marks center of detected object
	cv2.circle(vid2, (cx,cy), 2, (0,255,0),-1) # small green circle marks center of screen
    cv2.imshow("wctrl", vid2)
    cv2.waitKey(10)
    time.sleep(.1)

cv2.destroyAllWindows()
