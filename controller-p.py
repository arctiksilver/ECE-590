#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 7
# 11/7/14

# Reads from hw7-ik.txt and sends position coordinates to hw7.py

# ******************************************************

import hubo_ach as ha
import controller_include as ci
import ach
import os
import sys
import time
from ctypes import *

pos = ci.CONTROLLER_REF()

c = ach.Channel(ci.CONTROLLER_REF_NAME)
c.flush()
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
s.flush()
state = ha.HUBO_STATE()

def SimSleep(ts):
	s.get(state, wait=True, last=True)
	t = state.time + ts
	while(state.time < t):
		s.get(state, wait=True, last=True)
	return
# SimSleep

f = open('hw7-ik.txt', 'r')

while 1:
	for line in f:
		coordinates = line.split(" ")
		pos.x = float(coordinates[0])
		pos.y = float(coordinates[1])
		pos.z = float(coordinates[2])
		print "%f, %f, %f" % (pos.x, pos.y, pos.z)
		c.put(pos)
		SimSleep(3)
	f.seek(0)
f.close()
