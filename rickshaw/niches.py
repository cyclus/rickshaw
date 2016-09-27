# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:03:03 2016

@author: adam
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 14:18:30 2016

@author: adam

The function randomniche takes as input, the number of desired niches and the 
node that should act as the start point (with "mine" as the default startkey)
Produces a set containing the unique path.
"""

import random

#Dictionary of possible node connections, running the program creates a random node path, or niche
#Dictionary will need updating to account for new possible nodes

T = {
    "mine" : {"conversion", "enrichment", "hwr"},
    "conversion" : {"enrichment", "uo2_fabrication", "uo2_fabrication", "uo2_fabrication", "triso_fabrication", "hwr"}, 
    "enrichment" : {"uo2_fabrication", "triso_fabrication", "hwr", "fr"},
    "uo2_fabrication" : {"lwr", "htgr", "rbmk"},
    "triso_fabrication" : {"pb"},
    "fr" : {"storage", "dry_reprocessing", "purex", "deep_geological_repository", "near_surface_repository"},
    "lwr" : {"storage", "dry_reprocessing","purex","near_surface_repository", "deep_geological_repository"},
    "hwr" : {"storage", "near_surface_repository", "deep_geological_repository"},
    "htgr" : {"storage", "dry_reprocessing","purex","near_surface_repository", "deep_geological_repository"},         
    "rbmk" : {"storage", "dry_reprocessing","purex","near_surface_repository", "deep_geological_repository"},         
    "pb" : {"near_surface_repository", "deep_geological_repository"},         
    "storage" : {"dry_reprocessing","purex","near_surface_repository", "deep_geological_repository"},         
    "dry_reprocessing" : {"conversion","enrichment", "hwr", "mox_fabrication"},
    "purex" : {"conversion", "enrichment", "hwr", "mox_fabrication"},
    "mox_fabrication" : {"fr", "lwr", "htgr", "rbmk"},
    "deep_geological_repository" : {None},          
    "near_surface_repository" : {None} 
    }

#randomniche generates a set of possible nodes along a path of niches
#to change start point add new string in argument

def random_niches(max_niches, choice="mine", niches=None):
    if niches is None:
        niches = set()
    niches.add(choice)
    if max_niches == 1:
        return niches
    else:
        choice = random.sample(T[choice], 1)[0]
        if choice is None:
            return niches
        return random_niches(max_niches-1, choice, niches)
