#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*

# ******************************************************

# Chris Glomb
# Final Exam
# 12/16/14

# Waving control for ECE 590 Final Exam

# ******************************************************

import hubo_ach as ha
import controller_include_final as ci
import ach
import sys
import time
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
c = ach.Channel(ci.CONTROLLER_REF_NAME)
s.flush()
r.flush()
c.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# ach channel with walking control
com = ci.CONTROLLER_REF()

x = 0
y = 0
i = 0
st = 0
stop_time = 100
first = True

def SimSleep(ts, Ts):
	t = ts + Ts
	s.get(state, wait=False, last=False)	
	while(state.time < t):
		s.get(state, wait=True, last=False)
	return
# SimSleep


# Set initial arm position for waving
ref.ref[ha.LSR] = 1.5
ref.ref[ha.LSY] = 1.5
ref.ref[ha.LEB] = -0.8
ref.ref[ha.LWP] = 0.4
r.put(ref)

# wait for arm to arrive near initial waving  position
while state.joint[ha.LSR].pos < 1.4 or state.joint[ha.LSR].pos > 1.6:
	s.get(state, wait=False, last=False)
print "wave initial"

# sent start step command to walking control
com.val = ci.start_step
c.put(com)

# waving loop
while state.time < stop_time:
	if 0 == x:
		i = 0
		while i < 10:
			s.get(state, wait=False, last=True)
			r.get(ref, wait=False, last=True)
			ref.ref[ha.LEB] = ref.ref[ha.LEB] - 0.1
			ref.ref[ha.LWP] = ref.ref[ha.LWP] - 0.08
			r.put(ref)
			i += 1
			SimSleep(state.time, 0.1)
		x = 1
	else:
		i = 0
		while i < 10:
			s.get(state, wait=False, last=True)
			r.get(ref, wait=False, last=True)
			ref.ref[ha.LEB] = ref.ref[ha.LEB] + 0.1
			ref.ref[ha.LWP] = ref.ref[ha.LWP] + 0.08
			r.put(ref)
			i += 1
			SimSleep(state.time, 0.1)
		x = 0
		
	# check for message from walking control
	c.get(com, wait=False, last=True)
	if com.val == ci.step_complete and first:
		s.get(state, wait=False, last=True)
		stop_time = state.time + 5
		first = False
	print state.time, stop_time
	
print "wave complete"

# Set arm to return to start position
ref.ref[ha.LSR] = 0
ref.ref[ha.LSY] = 0
ref.ref[ha.LEB] = 0
ref.ref[ha.LWP] = 0
r.put(ref)

# command walking control to return to start position
com.val = ci.wave_complete
c.put(com)

SimSleep(state.time, 1)

# Close the connection to the channels
r.close()
s.close()
c.close()
