# -*- coding: utf-8 -*-
"""Modudle to help generate an archtypes list."""
import random

DEFAULT_SOURCES = {':agents:Source', ':cycamore:Source'}
DEFAULT_SINKS = {':agents:Sink', ':cycamore:Sink'}

NICHE_ARCHETYPES = {
    "mine": {},
    #"conversion" : {},
    "enrichment": {":agents:Enrichment"},
    "fuelfab:uo2_fabrication": {":agents:FuelFab"},
    "triso_fabrication": {":agents:FuelFab"},
    "reactor": {":agents:Reactor"},
    "reactor:fr": {":agents:Reactor"},
    "reactor:lwr": {":agents:Reactor"},
    "hwr": {":agents:Reactor"},
    "htgr": {":agents:Reactor"},
    "rbmk": {":agents:Reactor"},
    "pb": {":agents:Reactor"},
    "storage": {},
    "dry_reprocessing": {":agents:Separation"},
    "purex": {":agents:Separation"},
    "mox_fabrication": {":agents:FuelFab"},
    "deep_geological_repository": {":agents:Sink"},
    "near_surface_repository": {":agents:Sink"},
    }


def choose_archetypes(niches):
    arches = [random.choose(NICHE_ARCHETYPES[niches[0]] | DEFAULT_SOURCES)]
    for niche in niches[1:-1]:
        a = random.choose(NICHE_ARCHETYPES[niche])
        arches.append(a)
    if len(niches) > 1:
        a = random.choose(NICHE_ARCHETYPES[niches][-1] | DEFAULT_SINK)
        arches.append(a)
    return arches
