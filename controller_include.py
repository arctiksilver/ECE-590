#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 7 - IK
# 11/7/14

# ******************************************************

from ctypes import *


CONTROLLER_REF_NAME              = 'controller-ref-chan'

L_arm = 1
R_arm = 2
L_leg = 3
R_leg = 4

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("x",    c_float),
    		("y",    c_float),
    		("z",    c_float)]
