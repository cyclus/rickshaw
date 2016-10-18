# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:17:14 2016

@author: adam
"""


import random

def random_from_range(start, stop, step = 1):
    parameter = random.randrange(start, stop, step = 1) #step assumed to be 1
    return parameter