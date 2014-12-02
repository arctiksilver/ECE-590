#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 3
# 9/30/14

# this code uses robot-view-serial.py as the base

# ******************************************************

# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */
import diff_drive
import controller_include as ci
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import actuator_sim as ser
#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------


#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()
controller = ci.CONTROLLER_REF()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'

# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
c = ach.Channel(ci.CONTROLLER_REF_NAME)
c.flush()

i=0

ref.ref[0] = 0
ref.ref[1] = 0

def checksum(packet):
	j=0
	c=0
	l=5
	for byte in packet:
		if j == 3:
			l = byte
		if j > 1 and j < l+3:
			c += byte
		if j == (l + 3):
			c = ~c & 0xFF
			packet[j] = c
		j += 1
	return packet

def pack(motor,d,v):
	# motor - left = 1, right = 0
	# direction - forward = 1, reverse = 0
	#    0xFF, 0xFF, ID  , Length, Instruction   , Speed(L),        Speed(H)       , Checksum 
	p = [255 , 255 ,motor,   4   ,     0x20      ,  v&0xFF , ((v>>8)&0xFF)|(d<<2),     0    ]
	return checksum(p)

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

Ls = 0
Rs = 0

while 1:
	[statuss, framesizes] = c.get(controller, wait=True, last=False)
	
	if controller.dir == ci.FORWARD:
		Ls = 1000
		Rs = 1000
		buff = pack(1,1,Ls)
		ref = ser.serial_sim(r,ref,buff)
		buff = pack(0,1,Rs)
		ref = ser.serial_sim(r,ref,buff)
	elif controller.dir == ci.LEFT:
		if Ls >= 0:
			Ls = 500
			Rs = 1000
			buff = pack(1,1,Ls)
			ref = ser.serial_sim(r,ref,buff)
			buff = pack(0,1,Rs)
			ref = ser.serial_sim(r,ref,buff)
		else:
			Ls = -500
			Rs = -1000
			buff = pack(1,0,-Ls)
			ref = ser.serial_sim(r,ref,buff)
			buff = pack(0,0,-Rs)
			ref = ser.serial_sim(r,ref,buff)
	elif controller.dir == ci.BACK: # Stop / Reverse
		if Ls > 0 or Rs > 0: # If moving forward ramp down to stop
			for x in range(1000, -100, -100):
				buff = pack(1,1,x)
				ref = ser.serial_sim(r,ref,buff)
				buff = pack(0,1,x)
				ref = ser.serial_sim(r,ref,buff)
				simSleepTwentyHz(5)
				print x
			Ls = 0
			Rs = 0
		else: # if stoped then ramp up in reverse
			for x in range(1, 10):
				buff = pack(1,0,100*x)
				ref = ser.serial_sim(r,ref,buff)
				buff = pack(0,0,100*x)
				ref = ser.serial_sim(r,ref,buff)
				simSleepTwentyHz(10)
			Ls = -1000
			Rs = -1000
	elif controller.dir == ci.RIGHT:
		if Ls >= 0:
			Ls = 1000
			Rs = 500
			buff = pack(1,1,Ls)
			ref = ser.serial_sim(r,ref,buff)
			buff = pack(0,1,Rs)
			ref = ser.serial_sim(r,ref,buff)
		else:
			Ls = -1000
			Rs = -500
			buff = pack(1,0,-Ls)
			ref = ser.serial_sim(r,ref,buff)
			buff = pack(0,0,-Rs)
			ref = ser.serial_sim(r,ref,buff)
	print Ls , Rs

r.close()
t.close()
c.close()
