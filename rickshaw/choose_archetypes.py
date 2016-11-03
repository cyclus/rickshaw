# -*- coding: utf-8 -*-
"""Modudle to help generate an archtypes list."""
import random
global niches

from list_niches import random_niches

DEFAULT_SOURCES = {':agents:Source', ':cycamore:Source'}
DEFAULT_SINKS = {':agents:Sink', ':cycamore:Sink'}

NICHE_ARCHETYPES = {
    "mine": set(),
    #"conversion" : set(),
    "enrichment": {":cycamore:Enrichment"},
    "fuel_fab:uo2": {":cycamore:FuelFab"},
    "fuel_fab:triso": {":cycamore:FuelFab"},
    "reactor": {":cycamore:Reactor"},
    "reactor:fr": {":cycamore:Reactor"},
    "reactor:lwr": {":cycamore:Reactor"},
    "reactor:hwr": {":cycamore:Reactor"},
    "reactor:htgr": {":cycamore:Reactor"},
    "reactor:rbmk": {":cycamore:Reactor"},
    "reactor:pb": {":cycamore:Reactor"},
    "storage": set(),
    "separations": {":cycamore:Separation"},
    "fuel_fab:mox": {":cycamore:FuelFab"},
    "repository": set(),
    }


def choose_archetypes(niches):
    print(niches)
    arches = [random.choice(tuple(NICHE_ARCHETYPES[niches[0]] | DEFAULT_SOURCES))]
    for niche in niches[1:-1]:
        a = random.choice(tuple(NICHE_ARCHETYPES[niche]))
        arches.append(a)
    if len(niches) > 1:
        a = random.choice(tuple(NICHE_ARCHETYPES[niches][-1] | DEFAULT_SINKS))
        arches.append(a)
    return arches
    
def archetype_block(arches):
    unique_arches = sorted(set(arches))
    block = {"spec" : []}
    spec_keys = ["path", "lib", "name"]
    for a in unique_arches:
        spec = dict(zip(spec_keys, a.split(":")))
        block["spec"].append(spec)
    return block
