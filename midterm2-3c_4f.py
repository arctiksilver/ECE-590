#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*

# ******************************************************

# Chris Glomb
# Midterm 2
# 11/19/14

# ******************************************************

import numpy as np
import math
import matplotlib.pyplot as plt
import time

def FK(length = [], angle = []):
	T = np.matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
	if len(length) == len(angle):
		for i in range(0,len(length)):
			t = angle[i]
			d = length[i]
			#print t, d
			R = np.matrix(((math.cos(t), -math.sin(t), 0, 0), (math.sin(t), math.cos(t), 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
			D = np.matrix(((1, 0, 0, d), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
			Tx = R*D
			T = T*Tx
			#print T
		x = T[0,3]
		y = T[1,3]
	
	return x, y
# end FK



def IK(x,y):
	xpath = [.6]
	ypath = [0]
	delta = 0.005
	L = [.3, .2, .1]
	Theta = [0, 0, 0]
	cx, cy = FK(L, Theta)
	dist = math.sqrt(((x-cx)**2)+((y-cy)**2))
	count = 0
	while dist > 0.01 and count < 100:
		count += 1
		# compute jacobian
		J = np.zeros(shape=(3,2))
		for i in range(0,3):
			for j in range(0,2):
				if i == 0:
					nx, ny = FK(L, [Theta[0]+delta, Theta[1], Theta[2]])
				elif i == 1:
					nx, ny = FK(L, [Theta[0], Theta[1]+delta, Theta[2]])
				elif i == 2:
					nx, ny = FK(L, [Theta[0], Theta[1], Theta[2]+delta])
				if j == 0:
					J[i,j] = float(nx - cx)/delta
				if j == 1:
					J[i,j] = float(ny - cy)/delta
		
		# Jacobian psudo-inverse
		Ji = np.dot(np.linalg.inv(np.dot(J.transpose(), J)), J.transpose())
		e = np.array([(x-cx)/10,(y-cy)/10])
		dTheta = np.dot(e,Ji)
		
		# Bound values for dTheta
		if dTheta[0] > 0.2:
			dTheta[0] = 0.2
		elif dTheta[0] < -0.2:
			dTheta[0] = -0.2
		if dTheta[1] > 0.2:
			dTheta[1] = 0.2
		elif dTheta[1] < -0.2:
			dTheta[1] = -0.2
		if dTheta[2] > 0.2:
			dTheta[2] = 0.2
		elif dTheta[2] < -0.2:
			dTheta[2] = -0.2
		
		# Update angles
		Theta[0] += dTheta[0]
		Theta[1] += dTheta[1]
		Theta[2] += dTheta[2]
		
		# Record new x and y for plotting
		cx, cy = FK(L, Theta)
		dist = math.sqrt(((x-cx)**2)+((y-cy)**2))
		xpath = np.append(xpath,cx)
		ypath = np.append(ypath,cy)
	# Plot end effector path
	fig = plt.figure()
	ax = fig.add_subplot(111)
	p = ax.plot(xpath, ypath, 'b')
	ax.scatter(x,y, s=15, c='r', marker="o")
	ax.set_xlim(-0.8,0.8)
	ax.set_ylim(-0.8,0.8)
	ax.set_xlabel('x(m)')
	ax.set_ylabel('y(m)')
	ax.set_title('End Effector Path')
	plt.grid()
	fig.show()
	return Theta
# end IK

# **********************************************************************************

# Problem 3c - FK of variable length arm

print "\nProblem 3c\n\n"


# Set 1
L = [.1, .1, .1, .1, .1, .1, .1, .1, .1]
Th = [.1, .1, .1, .1, .1, .1, .1, .1, .1]

x, y = FK(L,Th)
print "Set 1: x = %f, y = %f" % (x,y)

# Set 2
L = [.3, .2, .1, .1, .2, .1, .3, .1, .1]
Th = [.4, .6, 1.2, .5, .1, .7, .3, .2, .1]

x, y = FK(L,Th)
print "Set 2: x = %f, y = %f" % (x,y)

# Set 3
L = [.1, .1, .1]
Th = [.1, .1, .1]

x, y = FK(L,Th)
print "Set 3: x = %f, y = %f" % (x,y)

# Set 4
L = [.1]
Th = [.4]

x, y = FK(L,Th)
print "Set 4: x = %f, y = %f" % (x,y)

# Set 5
L = [.2, .2, .2, .2, .2, .2, .2]
Th = [.2, .2, .2, .2, .2, .2, .2]

x, y = FK(L,Th)
print "Set 5: x = %f, y = %f" % (x,y)

# Set 6
L = [.3, .2, .1, .1, .2]
Th = [.4, .6, 1.2, .5, .1]

x, y = FK(L,Th)
print "Set 6: x = %f, y = %f" % (x,y)

# Set 7
L = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1]
Th = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1]

x, y = FK(L,Th)
print "Set 7: x = %f, y = %f" % (x,y)

# Set 8
L = [.3, .2, .1, .1, .2, .1, .3, .1, .1, .1, .1]
Th = [.4, .6, 1.2, .5, .1, .7, .3, .2, .1, .1, .1]

x, y = FK(L,Th)
print "Set 8: x = %f, y = %f" % (x,y)

# End of 3c

# **********************************************************************************

# Problem 4f - Jacobian IK
print "\n\nProblem 4f \n\nPlot Figure number corresponds to Set number\n"
# Set 1
th = IK(.1, .1)
print "Set 1: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 2
th = IK(.2, .2)
print "Set 2: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 3
th = IK(.3, .3)
print "Set 3: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 4
th = IK(0, .3)
print "Set 4: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 5
th = IK(-.1, .1)
print "Set 5: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 6
th = IK(-.2, .2)
print "Set 6: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 7
th = IK(.3, -.2)
print "Set 7: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])
# Set 8
th = IK(.3, .8)
print "Set 8: t1 = %f, t2 = %f, t3 = %f" % (th[0],th[1],th[2])

# While loops runs to prevent plots from disapearing when program ends
while 1:
	time.sleep(10)
