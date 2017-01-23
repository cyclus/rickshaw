# -*- coding: utf-8 -*-
"""Modudle to help generate an archtypes list."""
import random
import subprocess
import json


#from niches import niches

DEFAULT_SOURCES = {':agents:Source', ':cycamore:Source'}
DEFAULT_SINKS = {':agents:Sink', ':cycamore:Sink'}

NICHE_ARCHETYPES = {
    "mine": set(),
    #"conversion" : set(),
    "enrichment": {":cycamore:Enrichment"},
    "fuel_fab" : {":cycamore:FuelFab"},
    "fuel_fab:uo2": set(), #not the correct archetype currently possibly
    "fuel_fab:triso": {":cycamore:FuelFab"},
    "fuel_fab:mox": {":cycamore:FuelFab"},
    "reactor": {":cycamore:Reactor"},
    "reactor:fr": {":cycamore:Reactor"},
    "reactor:lwr": {":cycamore:Reactor"},
    "reactor:hwr": {":cycamore:Reactor"},
    "reactor:htgr": {":cycamore:Reactor"},
    "reactor:rbmk": {":cycamore:Reactor"},
    "reactor:pb": {":cycamore:Reactor"},
    "storage": set(),
    "storage:wet": set(),
    "storage:dry": set(),
    "storage:interim": set(),
    "separations": {":cycamore:Separation"},
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

def generate_archetype(arche, name):
    annotations = subprocess.check_output(["cyclus", "--agent-annotations", arche])
    annotations = json.loads(annotations)
    vals = {}
    for name, var in annotations.items():
        uitype = var.get("uitype", None)
        if uitype is None:
            continue
        if uitype == "range":
            if "nichedomain" in var:
                rng = var["nichedomain"].get(niche, var["range"])
            else:
                rng = var["range"]
            val = random.uniform(*rng)
            vals[name] = val
    alias = arche.rpartition(":")[-1]
    config = {"name": name, "config": {alias: vals}}
    return config


