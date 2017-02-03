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
from random import randrange

def choose_control():  
    
    
    duration = randrange(12, 600, 6)
    start_month = randrange(1, 12)
    start_year = randrange(2000, 2050)
    dt = randrange(2629846, 31558152, 2629846)
    
    control = {
    
                'duration' : duration,
                'startmonth' : start_month,
                'startyear' : start_year,
                'dt' : dt,
                
                }
                
    return control
    
    
    
    
    
    
