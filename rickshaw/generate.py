"""Generates a random Cyclus input file."""

import rickshaw.niches
import rickshaw.choose_control
import rickshaw.choose_archetypes


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
    niches = rickshaw.niches.random_niches(max_niches=max_num_niches)
    arches = rickshaw.choose_archtypes.choose_archetypes(niches)
    sim["archetypes"] = choose_archetypes.archetypes_block(arches)
    protos = {}
    for arche in arches:
        protos[arche] = choose_archetypes.generate_archetype(arche, name)
    sim["facility"] = list(protos.values())
    return inp

