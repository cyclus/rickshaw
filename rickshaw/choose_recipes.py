import random
from collections.abc import Sequence
from copy import deepcopy

NUCLIDES = {'natural_uranium': [{'id': 'U235', 'comp': 0.00711},
                                {'id': 'U238', 'comp': 0.99289}],
            'low_enriched_uranium': [{'id': 'U235', 'comp': [0.03, 0.05]},
                                     {'id': 'U238', 'comp': None}],
            'used_fuel': [{'id': 'U235', 'comp': [0.00650, 0.00720]},
                          {'id': 'U238', 'comp': None},
                          {'id': 'Pu238', 'comp': [0.000235, 0.000275]},
                          {'id': 'Pu239', 'comp': [0.00535, 0.00595]},
                          {'id': 'Pu240', 'comp': [0.00249, 0.00309]},
                          {'id': 'Pu241', 'comp': [0.00150, 0.00180]},
                          {'id': 'Pu242', 'comp': [0.000812, 0.000832]},
                          {'id': 'Am241', 'comp': [0.0000545, 0.0000565]},
                          {'id': 'Am243', 'comp': [0.000166, 0.000186]},
                          {'id': 'Cm242', 'comp': [0.0000223, 0.0000243]},
                          {'id': 'Cm244', 'comp': [0.0000696, 0.0000716]}]
           }

NUCLIDES['natural_uranium_fuel'] = NUCLIDES['natural_uranium']
NUCLIDES['stored_used_fuel'] = NUCLIDES['used_uox'] = NUCLIDES['used_fuel']

def interpolate(upper, lower):
    U = random.uniform(0, 1.0)
    interp = (upper - lower)*U + lower
    return interp

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
            the generated input file[]
    """
    recipes = []
    for commod in commods:
        recipe_dict = {}
        if commod not in NUCLIDES:
            continue
        recipe_dict['name'] = commod
        recipe_dict['basis'] = 'mass'
        nucs = recipe_dict['nuclide'] = deepcopy(NUCLIDES[commod])
        none_i = None
        total = 0.0
        u = random.uniform(0.0, 1.0)
        for i, nuc in enumerate(nucs):
            comp = nuc['comp']
            if isinstance(comp, float):
                total += comp
            elif comp is None:
                none_i = i
            elif isinstance(comp, Sequence):
                nuc['comp'] = comp = (comp[1] - comp[0])*u + comp[0]
                total += comp
        if none_i is not None:
            nucs[none_i]['comp'] = 1.0 - total
        recipes.append(recipe_dict)
    return recipes

def generate_nuclide(commod):
    pass
