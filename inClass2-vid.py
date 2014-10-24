#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# In Class Assignment 2
# 10/24/14

# this code uses robot-view-ctrl.py as the base

# ******************************************************

import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import controller_include as ci

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()
err = ci.CONTROLLER_REF()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

newx = 320
newy = 240

nx = 640
ny = 480

v = ach.Channel(ROBOT_CHAN_VIEW)
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
c = ach.Channel(ci.CONTROLLER_REF_NAME)

def SimSleep(ts, Ts):
	sleep = ts + Ts
	t.get(tim, wait=False, last=False)	
	while(tim.sim[0] < sleep):
		t.get(tim, wait=True, last=True)
	return
# SimSleep


i=0

while True:
    # Get sim time
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
    else:
        raise ach.AchException( v.result_string(status) )
    # Get Frame    
    img = np.zeros((newx,newy,3), np.uint8)
    c_image = img.copy()
    vid = cv2.resize(c_image,(newx,newy))
    [status, framesize] = v.get(vid, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vid,(nx,ny))
        img = cv2.cvtColor(vid2,cv2.COLOR_BGR2HSV)
    else:
        raise ach.AchException( v.result_string(status) )


    # apply threshold to get only blue pixels
    thresh = cv2.inRange(img, np.array((0.,80.,80.)), np.array((30.,255.,255.)))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2
        cv2.circle(img,(cx,cy), 2,[0, 0, 255],5)
        err.e = cx - nx/2
        c.put(err)
        print err.e
        centerStr = "e = %3.0f" % err.e
        cv2.putText(img,centerStr,(0,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
    cv2.imshow("wctrl", img)
    cv2.waitKey(10)
    
    SimSleep(tim.sim[0], 0.25)
