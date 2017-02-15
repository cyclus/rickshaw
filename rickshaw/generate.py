"""Generates a random Cyclus input file."""
import os
import json

from rickshaw import choose_niches
from rickshaw import choose_control
from rickshaw import choose_archetypes
from rickshaw import choose_recipes
from rickshaw import choose_commodities


def generate(max_num_niches=10):
    """Creates a random Cyclus simulation input file dict.

    Parameters
    ----------
    max_num_niches : int, optional
        The maximum number of niches in the simulation

    Returns
    -------
    inp : dict
        A simulation dictionary in JSON form, suitable for use
        as a Cyclus input file.
    """
    # intial structure
    inp = {"simulation": {}}
    sim = inp["simulation"]
    sim["control"] = choose_control.choose_control()
    # choose niches and archtypes
    niches = choose_niches.random_niches(max_niches=max_num_niches)
    arches = choose_archetypes.choose_archetypes(niches)
    commods = choose_commodities.choose_commodities(niches)
    recipes = choose_recipes.choose_recipes(commods)
    if len(recipes) == 1:
        recipes = recipes[0]
    sim["archetypes"] = choose_archetypes.archetype_block(arches)
    #put the other things in here
    sim["recipe"] = recipes
    protos = {}
    protos[arches[0]] = choose_archetypes.generate_archetype(arches[0], None,
                                                         commods[0])

    for arche, in_commod, out_commod in zip(arches[1:-1], commods[:-1],
                                            commods[1:]):
        protos[arche] = choose_archetypes.generate_archetype(arche, in_commod,
                                                             out_commod)

    protos[arches[-1]] = choose_archetypes.generate_archetype(arches[-1],
                                                         commods[-1], None)
    sim["facility"] = list(protos.values())
    return inp

