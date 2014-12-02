#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 3
# 9/30/14

# ******************************************************

import controller_include as ci
import ach
import os
import sys
import termios
import fcntl
from ctypes import *


c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller = ci.CONTROLLER_REF()

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
	controller.dir = getch()
	c.put(controller)

c.close()
