#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# Final Exam
# 12/16/14

# ******************************************************

from ctypes import *


CONTROLLER_REF_NAME              = 'controller-ref-chan'

start_step = 1
step_complete = 2
wave_complete = 3

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("val",    c_byte)]
