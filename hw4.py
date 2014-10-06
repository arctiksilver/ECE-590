#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*

# ******************************************************

# Chris Glomb
# Homework 4
# 10/7/14

# this code uses the hubo-simple-demo-python as the base

# ******************************************************

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()


def SimSleep(ts, Ts):
	t = ts + Ts
	s.get(state, wait=False, last=False)	
	while(state.time < t):
		s.get(state, wait=True, last=False)
	return
# SimSleep


x = 0
y = 0
t = 0
i = 0
shift = 14

# get in walking position
while i < 5:
	s.get(state, wait=False, last=False)
	x += 0.1
	ref.ref[ha.LHP] = -x
        ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = -x
        ref.ref[ha.RHP] = -x
        ref.ref[ha.RKN] = 2*x
        ref.ref[ha.RAP] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.2)

x = 0
i = 0
# shift weight to right foot
while i < shift:
	s.get(state, wait=False, last=False)
	x += 0.01
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# raise up on right leg
i = 0
while i < 3:
	s.get(state, wait=False, last=False)
	x = 0.04
	ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RKN] = ref.ref[ha.RKN] - 2*x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# take first step forward with left leg
i = 0
x = 0.01
while i < 6:
	# left foot forward
	ref.ref[ha.LHP] = ref.ref[ha.LHP] - x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
        # right foot back
        ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - x
        # right leg down
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - .02
        ref.ref[ha.RKN] = ref.ref[ha.RKN] + .04
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
x = 0.01
i = 0
# shift weight to left foot
while i < 2*shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] - x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] - x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] + x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# raise up on left leg
i = 0
while i < 3:
	s.get(state, wait=False, last=False)
	x = 0.04
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LKN] = ref.ref[ha.LKN] - 2*x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)
	
# take step forward with right leg
i = 0
x = 0.025
while i < 6:
	# left foot back
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - x
        # right foot forward
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
        # left leg down
        ref.ref[ha.LHP] = ref.ref[ha.LHP] - .02
        ref.ref[ha.LKN] = ref.ref[ha.LKN] + .04
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

i = 0
x = 0.01
# shift weight to right foot
while i < 2*shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] + x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] + x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] - x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] - x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
# raise up on right leg
i = 0
x = 0.04
while i < 3:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RKN] = ref.ref[ha.RKN] - 2*x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# take step forward with left leg
i = 0
x = 0.025
while i < 6:
	# left foot forward
	ref.ref[ha.LHP] = ref.ref[ha.LHP] - x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
        # right foot back
        ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - x
        # right leg down
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - .02
        ref.ref[ha.RKN] = ref.ref[ha.RKN] + .04
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
x = 0.01
i = 0
# shift weight to left foot
while i < 2*shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] - x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] - x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] + x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# raise up on left leg
i = 0
x = 0.04
while i < 3:
	s.get(state, wait=False, last=False)
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LKN] = ref.ref[ha.LKN] - 2*x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)
	
# take step forward with right leg
i = 0
x = 0.025
while i < 6:
	# left foot back
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - x
        # right foot forward
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
        # left leg down
        ref.ref[ha.LHP] = ref.ref[ha.LHP] - .02
        ref.ref[ha.LKN] = ref.ref[ha.LKN] + .04
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
i = 0
x = 0.01
# shift weight to right foot
while i < 2*shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] + x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] + x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] - x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] - x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
# raise up on right leg
i = 0
x = 0.04
while i < 3:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RKN] = ref.ref[ha.RKN] - 2*x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# take step forward with left leg
i = 0
x = 0.025
while i < 6:
	# left foot forward
	ref.ref[ha.LHP] = ref.ref[ha.LHP] - x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
        # right foot back
        ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - x
        # right leg down
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - .02
        ref.ref[ha.RKN] = ref.ref[ha.RKN] + .04
        ref.ref[ha.RAP] = ref.ref[ha.RAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
x = 0.01
i = 0
# shift weight to left foot
while i < 2*shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] - x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] - x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] + x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# raise up on left leg
i = 0
x = 0.04
while i < 3:
	s.get(state, wait=False, last=False)
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LKN] = ref.ref[ha.LKN] - 2*x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)
	
# take step forward with right leg
i = 0
x = 0.025
while i < 6:
	# left foot back
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - x
        # right foot forward
        ref.ref[ha.RHP] = ref.ref[ha.RHP] - x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
        # left leg down
        ref.ref[ha.LHP] = ref.ref[ha.LHP] - .02
        ref.ref[ha.LKN] = ref.ref[ha.LKN] + .04
        ref.ref[ha.LAP] = ref.ref[ha.LAP] - .02
        r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
i = 0
x = 0.01
# shift weight to center
while i < shift:
	s.get(state, wait=False, last=False)
	ref.ref[ha.RHR] = ref.ref[ha.RHR] + x
	ref.ref[ha.LHR] = ref.ref[ha.LHR] + x
	ref.ref[ha.RAR] = ref.ref[ha.RAR] - x
	ref.ref[ha.LAR] = ref.ref[ha.LAR] - x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

i = 0
x = 0.1
# stand back up
while i < 5:
	s.get(state, wait=False, last=False)
	ref.ref[ha.LHP] = ref.ref[ha.LHP] + x
        ref.ref[ha.LKN] = ref.ref[ha.LKN] - 2*x
        ref.ref[ha.LAP] = ref.ref[ha.LAP] + x
        ref.ref[ha.RHP] = ref.ref[ha.RHP] + x
        ref.ref[ha.RKN] = ref.ref[ha.RKN] - 2*x
        ref.ref[ha.RAP] = ref.ref[ha.RAP] + x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.2)	

# Close the connection to the channels
r.close()
s.close()
