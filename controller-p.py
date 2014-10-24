#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# In Class Assignment 2 - PID Controller
# 10/24/14

# ******************************************************

import diff_drive
import controller_include as ci
import ach

from ctypes import *

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_TIME_CHAN  = 'robot-time'

c = ach.Channel(ci.CONTROLLER_REF_NAME)
err = ci.CONTROLLER_REF()
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()
lastE = 0
lastT = 0
p = 0
i = 0
d = 0

while 1:
	[status, framesize] = c.get(err, wait=True, last=True)
	[status, framesize] = t.get(tim, wait=False, last=True)
	# Praportional Control
	p = float(err.e)
	
	# Integral Control
	i += p
	
	# Derivative Control
	d = float(err.e - lastE) / (tim.sim[0] - lastT)
	lastE = err.e
	lastT = tim.sim[0]
	
	# Controller output
	output = float(p + i*0.3 + d*0.4) / 320
	
	if output > 1:
		output = 1
	elif output < -1:
		output = -1
	print "%3.2f, %3.2f" % (tim.sim[0],err.e)
	
	ref.ref[0] = -output
    	ref.ref[1] = output

    	r.put(ref)
    	

c.close()
r.close()
t.close()
