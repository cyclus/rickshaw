# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:17:14 2016

@author: adam

This program will choose the control scheme at random for a cyclus input file in json
Parameters to choose at random:

duration (in months)
start month (jan = 1, dec = 12)
start year (starting at 2000)
dt time step (in seconds)

"""

from random_from_range import random_from_range



def choose_control():  
    
    
    duration = random_from_range(12, 600, 6)
    start_month = random_from_range(1, 12)
    start_year = random_from_range(2000, 2050)
    dt = random_from_range(2,629,846, 31,558,152, 2,629,846)
    
    control = {
    
                'duration' : duration,
                'startmonth' : start_month,
                'startyear' : start_year,
                'dt' : dt,
                
                }
                
    return control
    
    
    
    
    
    
