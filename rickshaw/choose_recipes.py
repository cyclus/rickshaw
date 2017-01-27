def choose_recipes(commods):
    recipes = []
    for commod in commods:
        recipe_dict = {}
        commod_base = commod[0]
        commod_name = commod[1]
        recipe_dict['name'] = commod_name
        recipe_dict['basis'] = 'mass'
        recipe_dict['nuclide'] = NUCLIDES[commod_base]

NUCLIDES = {'natural_uranium': [{'id': 'U235', 'comp': 0.007},
                                {'id': 'U238', 'comp': 0.993}],
            'low_enriched_uranium': [{'id': 'U235', 'comp': 0.05},
                                     {'id': 'U238', 'comp': 0.95}],
            
           }

def generate_nuclide(commod):
    pass
