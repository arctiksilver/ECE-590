#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Homework 3
# 9/30/14

# ******************************************************

from ctypes import *

FORWARD = 'w'
LEFT = 'a'
BACK = 's'
RIGHT = 'd'


CONTROLLER_REF_NAME              = 'controller-ref-chan'

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("dir",    c_char*1)]
