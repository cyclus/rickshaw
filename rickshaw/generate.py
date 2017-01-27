"""Generates a random Cyclus input file."""

import niches
import choose_control
import choose_archetypes


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
    sim["control"] = rickshaw.choose_control.choose_control()
    # choose niches and archtypes
    niches = niches.random_niches(max_niches=max_num_niches)
    arches = choose_archetypes.choose_archetypes(niches)
    commods = choose_commodities.choose_commodities(niches)
    commod_names = [x[1] for x in commods]
    recipes = choose_recipes.choose_recipes(commods)
    sim["archetypes"] = choose_archetypes.archetypes_block(arches)
    protos = {}
    protos[arche] = choose_archetypes.generate_archetype(arches[0], name, None, 
                                                         commod_names[0])
    
    for arche, in_commod, out_commod in zip(arches[1:-1], commod_names[:-1], 
                                            commod_names[1:]):
        protos[arche] = choose_archetypes.generate_archetype(arche, name, 
                                                             commod_names)
    
    protos[arche] = choose_archetypes.generate_archetype(arches[-1], name, 
                                                         commod_names[-1], None)
    sim["facility"] = list(protos.values())
    return inp

