"""
Created on Wed Dec 28 13:19:28 2016

@author: adam
"""
import random

COMMODITIES = {
    ("mine", "enrichment"): "natural_uranium",
    ("mine", "reactor:hwr"): "natural_uranium_fuel",
    ("enrichment", "fuel_fab"): "low_enriched_uranium",
    ("enrichment", "repository"): "enrichment_waste_stream",
    ("fuel_fab", "reactor"): "fresh_fuel",
    ("fuel_fab:uo2", "reactor:lwr"): "fresh_uox",
    ("fuel_fab:triso", "reactor:pb"): "fresh_triso",
    ("reactor", "storage"): "used_fuel",
    ("reactor", "repository"): "used_fuel",
    ("reactor:lwr", "storage"): "used_uox",
    ("reactor:pb", "storage"): "used_triso",
    ("reactor", "separations"): "used_fuel",
    ("reactor:lwr", "separations"): "used_uox",
    ("storage", "separations"): "stored_used_fuel",
    ("storage", "repository"): "stored_used_fuel",
    ("separations", "fuel_fab"): "separated_product",
    ("separations", "storage"): "separated_waste",
    ("separations", "repository"): "separated_waste"
}

def up_hierarchy(key):
    #If we have it, immediately return
    if key in COMMODITIES:
        return COMMODITIES[key]
    #If the key contains a colon, we may be able to provide a more basic form
    if ":" in key[0]:
        keyfrom, _, _ = key[0].rpartition(":")
    else:
        keyfrom = key[0]
    if ":" in key[1]:
        keyto, _, _ = key[1].rpartition(":")
    else:
        keyto = key[1]
    #If our new key is identical to the original, we can't support it
    if (keyfrom, keyto) == key:
        return None
    else:
        if (keyfrom, key[1]) != key:
            commod = up_hierarchy((keyfrom, key[1]))
            if commod is not None:
                return commod
        if (key[0], keyto) != key:
            commod = up_hierarchy((key[0], keyto))
            if commod is not None:
                return commod
        commod = up_hierarchy((keyfrom, keyto))
        return commod
    
def choose_commodity(keyfrom, keyto, unique_commods):
    """Determine commodity based on a from/to pairs.
    
    Parameters
    ----------
    keyfrom : str
        Origin niche name.
    keyto : str
        Following niche name.
    unique_commods : set
        Current names used by chosen commodities.
    
    Returns
    -------
    commod_name : str
        A unique commodity name.
    """
    commod = orig_commod = up_hierarchy((keyfrom, keyto))
    if commod is None:
        return None
    n = 1
    commod_name = commod
    while commod_name in unique_commods:
        commod_name = orig_commod + str(n)
        n = n + 1
    unique_commods.add(commod_name)
    return commod_name

def choose_commodities(niches):
    """Creates list of commodities individually chosen by the choose_commodity function
    
    Parameters
    ----------
    niches : list
        List of sequential niches returned from choose_niches.py
    
    Returns
    -------
    commods : list
        List of in and out commodities to be added to the archetypes in the
        input file.
    """
    commods = []
    unique_commods = set()
    for keyfrom, keyto in zip(niches[:-1], niches[1:]):
        commod = choose_commodity(keyfrom, keyto, unique_commods)
        if commod is None:
            continue
        commods.append(commod)
    return commods

