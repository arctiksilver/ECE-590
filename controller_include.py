#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb, Christian Gibbons, Michael Reyes
# In Class Assignment 3
# 11/18/14

# ******************************************************

from ctypes import *


CONTROLLER_REF_NAME             = 'controller-ref-chan'
DYNAMIXL_CTRL_NAME 		= 'dynamixl-ctrl-chan'

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("x",    c_int),
    		("y",    c_int)]
    		
class DYNAMIXL_REF(Structure):
    _pack_ = 1
    _fields_ = [("yaw_dir",     c_float),
    		("yaw_speed",   c_int),
    		("pitch_dir",   c_float),
    		("pitch_speed", c_int)]
