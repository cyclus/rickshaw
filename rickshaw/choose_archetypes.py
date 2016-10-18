# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:59:19 2016

@author: adam
"""

NICHE_ARCHETYPES = {
    "mine" : {":agents:Source"},
    "conversion" : {":agents:Source", ":agents:Sink"},
    "enrichment" : {":agents:Source", ":agents:Sink", ":agents:Enrichment"},
    "uo2_fabrication" : {":agents:Source", ":agents:Sink", ":agents:FuelFab"},
    "triso_fabrication" : {":agents:Source", ":agents:Sink", ":agents:FuelFab"},
    "fr" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "lwr" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "hwr" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "htgr" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "rbmk" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "pb" : {":agents:Source", ":agents:Sink", ":agents:Reactor"},
    "storage" : {":agents:Source", ":agents:Sink"},
    "dry_reprocessing" : {":agents:Source", ":agents:Sink", ":agents:Separation"},
    "purex" : {":agents:Source", ":agents:Sink", ":agents:Separation"},
    "mox_fabrication" : {":agents:Source", ":agents:Sink", ":agents:FuelFab"},
    "deep_geological_repository" : {":agents:Sink"},       
    "near_surface_repository" : {":agents:Sink"}
    }

from niches import niches
import random

def choose_archetypes():
    arche = []
    for niche in niches:
        a = random.choose(NICHE_ARCHETYPES[niche])
        arche.append(a)
    return arche
    
    