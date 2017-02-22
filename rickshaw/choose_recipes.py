NUCLIDES = {'natural_uranium': [{'id': 'U235', 'comp': 0.007},
                                {'id': 'U238', 'comp': 0.993}],
            'low_enriched_uranium': [{'id': 'U235', 'comp': 0.05},
                                     {'id': 'U238', 'comp': 0.95}],
            'used_fuel': [{'id': 'U235', 'comp': .00696},
                          {'id': 'U238', 'comp': .927},
                          {'id': 'Pu238', 'comp': .000255},
                          {'id': 'Pu239', 'comp': .00565},
                          {'id': 'Pu240', 'comp': .00279},
                          {'id': 'Pu241', 'comp': .00163},
                          {'id': 'Pu242', 'comp': .000822},
                          {'id': 'Am241', 'comp': .0000555},
                          {'id': 'Am243', 'comp': .000176},
                          {'id': 'Cm242', 'comp': .0000233},
                          {'id': 'Cm244', 'comp': .0000706}]
           }

NUCLIDES['natural_uranium'] = NUCLIDES['natural_uranium_fuel']
NUCLIDES['stored_used_fuel'] = NUCLIDES['used_uox'] = NUCLIDES['used_fuel'] 

def choose_recipes(commods):
    """Chooses the specific recipe for each commodity in the commods list
    
    Parameters
    ----------
        commods : list
            List of in and out commodities to be added to the archetypes in the
            input file.
    
    Returns
    -------
        recipes : list
            List of the assigned recipes to be added to the recipe section of 
            the generated input file
    """
    recipes = []
    for commod in commods:    
        recipe_dict = {}
        if commod not in NUCLIDES:
            continue
        recipe_dict['name'] = commod
        recipe_dict['basis'] = 'mass'
        recipe_dict['nuclide'] = NUCLIDES[commod]
        recipes.append(recipe_dict)
    return recipes

def generate_nuclide(commod):
    pass
