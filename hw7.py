#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*

# ******************************************************

# Chris Glomb
# Homework 7
# 10/7/14

# ******************************************************

import hubo_ach as ha
import controller_include as ci
import numpy as np
import ach
import sys
import time
import math
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
c = ach.Channel(ci.CONTROLLER_REF_NAME)
#s.flush()
#r.flush()
c.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# x,y,z hand position data
pos = ci.CONTROLLER_REF()

def SimSleep(ts):
	s.get(state, wait=True, last=True)
	t = state.time + ts
	while(state.time < t):
		s.get(state, wait=True, last=True)
	return
# SimSleep
RSP_max = 1
RSP_min = -2.8
RSY_max = 1
RSY_min = -1
RSR_max = 0.2
RSR_min = -2.5
REB_max = 0.1
REB_min = -2

def FK(Theta1, Theta2, Theta3, Theta4,limb):
#      Pitch , Yaw   , Role  , Bend
	if limb == ci.R_arm:
		x0,y0,z0 = -.215,0,0 # limb origin
		l1 = -0.179 # upper segment length
		l2 = -0.182 # lower segment length
		t1 = Theta1 + 0 # Angle offsets
		t2 = Theta2 + 0
		t3 = Theta3 - 0.2
		t4 = Theta4 - 0.1
	elif limb == ci.L_arm:
		x0,y0,z0 = .215,0,0
		l1 = -0.179
		l2 = -0.182
		t1 = Theta1 + 0
		t2 = Theta2 + 0
		t3 = Theta3 + 0.2
		t4 = Theta4 - 0.1

	
	position = ci.CONTROLLER_REF()
	
	Rx1 = np.matrix(((1, 0, 0, 0), (0, math.cos(t1), -math.sin(t1), 0), (0, math.sin(t1), math.cos(t1), 0), (0, 0, 0, 1)))
	Ry = np.matrix(((math.cos(t2), 0, math.sin(t2), 0), (0, 1, 0, 0), (-math.sin(t2), 0, math.cos(t2), 0), (0, 0, 0, 1)))
	Rz = np.matrix(((math.cos(t3), -math.sin(t3), 0, 0), (math.sin(t3), math.cos(t3), 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
	Rx2 = np.matrix(((1, 0, 0, 0), (0, math.cos(t4), -math.sin(t4), 0), (0, math.sin(t4), math.cos(t4), 0), (0, 0, 0, 1)))

	D1 = np.matrix(((1,0,0,0),(0,1,0,l1),(0,0,1,0),(0,0,0,1)))
	D2 = np.matrix(((1,0,0,0),(0,1,0,l2),(0,0,1,0),(0,0,0,1)))

	T1 = Rx1*Ry*Rz*D1
	T2 = Rx2*D2
	
	T= T1*T2
	
	position.x = T[0,3] + x0
	position.y = T[1,3] + y0
	position.z = T[2,3] + z0
	
	#print Theta1,Theta2,Theta3,Theta4
	#print T1, T2
	#print position.x,position.y,position.z
	
	return position
# end FK
	

def IK(x,y,z,limb):
	# Get desired limb joint values
	s.get(state, wait=True, last=True)
	if limb == ci.R_arm:
		P,Y,R,B = state.joint[ha.RSP].pos,state.joint[ha.RSY].pos,state.joint[ha.RSR].pos,state.joint[ha.REB].pos
		#P,Y,R,B = ref.ref[ha.RSP], ref.ref[ha.RSY], ref.ref[ha.RSR], ref.ref[ha.REB]
	elif limb == ci.L_arm:
		P,Y,R,B = state.joint[ha.LSP].pos,state.joint[ha.LSY].pos,state.joint[ha.LSR].pos,state.joint[ha.LEB].pos
		#P,Y,R,B = ref.ref[ha.LSP], ref.ref[ha.LSY], ref.ref[ha.LSR], ref.ref[ha.LEB]
	elif limb == ci.R_leg:
		P,Y,R,B = state.joint[ha.RHP].pos,state.joint[ha.RHY].pos,state.joint[ha.RHR].pos,state.joint[ha.RKN].pos
	elif limb == ci.L_leg:
		P,Y,R,B = state.joint[ha.LHP].pos,state.joint[ha.LHY].pos,state.joint[ha.LHR].pos,state.joint[ha.LKN].pos
	# determine distance to target
	current = FK(P,Y,R,B,limb)
	#print "current: %1.3f %1.3f %1.3f" % (current.x, current.y, current.z)
	dist = math.sqrt(((x-current.x)**2)+((y-current.y)**2)+((z-current.z)**2))
	if dist > 0.03:
		e = np.array([(x-current.x)/8,(y-current.y)/8,(z-current.z)/8])
		# compute jacobian
		delta = 0.05
		J = np.zeros(shape=(4,3))
		for i in range(0,4):
			for j in range(0,3):
				if i == 0:
					new = FK(P+delta,Y,R,B,limb)
				elif i == 1:
					new = FK(P,Y+delta,R,B,limb)
				elif i == 2:
					new = FK(P,Y,R+delta,B,limb)
				elif i == 3:
					new = FK(P,Y,R,B+delta,limb)
				if j == 0:
					J[i,j] = float(new.x - current.x)/delta
				if j == 1:
					J[i,j] = float(new.y - current.y)/delta
				if j == 2:
					J[i,j] = float(new.z - current.z)/delta
		
		Ji = np.dot(np.linalg.inv(np.dot(J.transpose(), J)), J.transpose())
		#Ji = J.transpose()
		dTheta = np.dot(e,Ji)
		for i in range(0,4):
			dTheta[i] = dTheta[i]/1.0
			if dTheta[i] > 0.2:
				dTheta[i] = 0.2
			elif dTheta[i] < -0.2:
				dTheta[i] = -0.2
		if limb == ci.R_arm:
			ref.ref[ha.RSP] = P + dTheta[0]
			ref.ref[ha.RSY] = Y + dTheta[1]
			ref.ref[ha.RSR] = R + dTheta[2]
			ref.ref[ha.REB] = B + dTheta[3]
		elif limb == ci.L_arm:
			ref.ref[ha.LSP] = P + dTheta[0]
			ref.ref[ha.LSY] = Y + dTheta[1]
			ref.ref[ha.LSR] = R + dTheta[2]
			ref.ref[ha.LEB] = B + dTheta[3]
		elif limb == ci.R_leg:
			ref.ref[ha.RHP] = P + dTheta[0]
			ref.ref[ha.RHY] = Y + dTheta[1]
			ref.ref[ha.RHR] = R + dTheta[2]
			ref.ref[ha.RKN] = B + dTheta[3]
		elif limb == ci.L_leg:
			ref.ref[ha.LHP] = P + dTheta[0]
			ref.ref[ha.LHY] = Y + dTheta[1]
			ref.ref[ha.LHR] = R + dTheta[2]
			ref.ref[ha.LKN] = B + dTheta[3]
		
		if ref.ref[ha.RSR] < -1.5:
			ref.ref[ha.RSR] = -1.5
		elif ref.ref[ha.RSR] > .2:
			ref.ref[ha.RSR] = .2
		if ref.ref[ha.LSR] < -1.5:
			ref.ref[ha.LSR] = -1.5
		elif ref.ref[ha.LSR] > .2:
			ref.ref[ha.LSR] = .2
		#if ref.ref[ha.RSY] < -.5:
		#	ref.ref[ha.RSY] = -.5
		#elif ref.ref[ha.RSY] > .5:
		#	ref.ref[ha.RSY] = .5
		#if ref.ref[ha.LSY] < -.5:
		#	ref.ref[ha.LSY] = -.5
		#elif ref.ref[ha.LSY] > .5:
		#	ref.ref[ha.LSY] = .5
		
		r.put(ref)
		#print "%1.3f, %1.3f, %1.3f, %1.3f, %1.3f" % (dist, ref.ref[ha.RSP], ref.ref[ha.RSY], ref.ref[ha.RSR], ref.ref[ha.REB])
			
# end IK

# wait for first position from controller
c.get(pos, wait=True, last=True)		
while 1:
	c.get(pos, wait=False, last=True)
	IK(pos.x, pos.y, pos.z,ci.R_arm)
	IK(-pos.x, pos.y, pos.z,ci.L_arm)
	SimSleep(0.1)


# Close the connection to the channels
r.close()
s.close()
c.close()
