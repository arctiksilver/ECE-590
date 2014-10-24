#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */

# ******************************************************

# Chris Glomb
# In Class Assignment 2
# 10/24/14

# ******************************************************

from ctypes import *


CONTROLLER_REF_NAME              = 'controller-ref-chan'

class CONTROLLER_REF(Structure):
    _pack_ = 1
    _fields_ = [("e",    c_int)]
