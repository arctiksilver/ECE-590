#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 6
# 10/28/14

# ******************************************************

import diff_drive
import ach
import os
import sys
import termios
import fcntl
from ctypes import *


dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_TIME_CHAN  = 'robot-time'

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

Ls = 0
Rs = 0

def simSleepTwentyHz(duration):
	i = 0
	[status, framesize] = t.get(tim, wait=True, last=True)
	next = tim.sim[0] + 0.05
	while i < duration:
		[status, framesize] = t.get(tim, wait=True, last=True)
		while tim.sim[0] < next:
			[status, framesize] = t.get(tim, wait=True, last=True)
			if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
				pass
			else:
				raise ach.AchException( v.result_string(status) )
		next = tim.sim[0] + 0.05
		[status, framesize] = t.get(tim, wait=True, last=True)
		i += 1

# The getch() function is from http://love-python.blogspot.com/2010/03/getch-in-python-get-single-character.html
def getch():
	fd = sys.stdin.fileno()
	
	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
	
	try:        
		while 1:            
			try:
				direction = sys.stdin.read(1)
				break
			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return direction

while 1:
    c = getch()
	
    if c == 'w':
	Ls = 1000
	Rs = 1000
	for x in range(1, 5):
		ref.ref[0] = float(x)/10
		ref.ref[1] = float(x)/10
		r.put(ref)
		print ref.ref[0]
		simSleepTwentyHz(10)
    elif c == 'a':
	if Ls >= 0:
		Ls = 500
		Rs = 1000
		ref.ref[0] = 0.5
		ref.ref[1] = 0.25
		r.put(ref)
	else:
		Ls = -500
		Rs = -1000
		ref.ref[0] = -0.5
		ref.ref[1] = -0.25
		r.put(ref)
    elif c == 's': # Stop / Reverse
	if Ls > 0 or Rs > 0: # If moving forward ramp down to stop
		for x in range(5, -1, -1):
			ref.ref[0] = float(x)/10
			ref.ref[1] = float(x)/10
			r.put(ref)
			simSleepTwentyHz(10)
		Ls = 0
		Rs = 0
	else: # if stoped then ramp up in reverse
		for x in range(1, 5):
			ref.ref[0] = -float(x)/10
			ref.ref[1] = -float(x)/10
			r.put(ref)
			simSleepTwentyHz(10)
		Ls = -1000
		Rs = -1000
    elif c == 'd':
	if Ls >= 0:
		Ls = 1000
		Rs = 500
		ref.ref[0] = 0.25
		ref.ref[1] = 0.5
	else:
		Ls = -1000
		Rs = -500
		ref.ref[0] = -0.25
		ref.ref[1] = -0.5

r.close()
t.close()
