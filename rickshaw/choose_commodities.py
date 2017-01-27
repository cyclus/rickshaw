"""
Created on Wed Dec 28 13:19:28 2016

@author: adam
"""
import random

COMMODITIES = {
    ("mine", "enrichment"): "natural uranium",
    ("enrichment", "fuel_fab"): "low enriched uranium",
    ("enrichment", "repository"): "enrichment waste stream",
    ("fuel_fab", "reactor"): "fresh fuel",
    ("fuel_fab:uo2", "reactor:lwr"): "fresh uox",
    ("fuel_fab:triso", "reactor:pb"): "fresh triso",
    ("reactor", "storage"): "used fuel",
    ("reactor", "repository"): "used fuel",
    ("reactor:lwr", "storage"): "used uox",
    ("reactor:pb", "storage"): "used triso",
    ("reactor", "separations"): "used fuel",
    ("reactor:lwr", "separations"): "used uox",
    ("storage", "separations"): "stored used fuel",
    ("storage", "repository"): "stored used fuel",
    ("separations", "fuel_fab"): "separated product",
    ("separations", "storage"): "separated waste",
    ("separations", "repository"): "separated waste"
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
    while commod in unique_commods:
        commod = orig_commod + str(n)
        n = n + 1
    unique_commod.add(commod)
    return commod
