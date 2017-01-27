"""
Created on Wed Dec 28 13:19:28 2016

@author: adam
"""
import random

COMMODITIES = {
    ("mine", "enrichment"): "natural_uranium",
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
    if key in COMMODITIES:
        return COMMODITIES[key]
    if ":" in key[0]:
        keyfrom, _, _ = key[0].rpartition(":")
    else:
        keyfrom = key[0]
    if ":" in key[1]:
        keyto, _, _ = key[1].rpartition(":")
    else:
        keyto = key[1]
    if (keyfrom, keyto) == key:
        return None
    commod = up_hierarchy(COMMODITIES, (keyfrom, key[1]))
    if commod is not None:
        return commod
    commod = up_hierarchy(COMMODITIES, (key[0], keyto))
    if commod is not None:
        return commod
    commod = up_hierarchy(COMMODITIES, (keyfrom, keyto))
    return commod
    
def choose_commodity(keyfrom, keyto, unique_commods):
    commod = orig_commod = up_hierarchy((keyfrom, keyto))
    n = 1
    commod_name = commod
    while commod_name in unique_commods:
        commod_name = orig_commod + str(n)
        n = n + 1
    unique_commods.add(commod_name)
    return commod, commod_name

def choose_commodities(niches):
    commods = []
    unique_commods = set()
    for keyfrom, keyto in zip(niches[:-1], niches[1:]):
        commod = choose_commidity(keyfrom, keyto, unique_commods)
        commods.append(commod)
    return commods

