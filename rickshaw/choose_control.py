from random import randrange

def choose_control():  
    """This program will choose the control scheme at random for a cyclus 
    input file in JSON
    
    Returns
    -------
        control : dict
            Dictionary generated to be the control scheme in the JSON cyclus
            input file
    """    
    
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
    
    
    
    
    
    
