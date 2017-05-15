# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:49:39 2016

@author: adam
"""
import pytest
from rickshaw.simspec import SimSpec, def_niches, def_commodities
from rickshaw.generate import random_niches, choose_commodity, choose_commodities

@pytest.mark.parametrize("i", range(100))
def test_random_niches(i):
    spec = SimSpec()
    obs = random_niches(spec, 10)
    assert isinstance(obs, list)
    assert "mine" in obs
    assert None not in obs
    assert len(obs) <= 10
    for niche in obs:
        assert niche in def_niches()

@pytest.mark.parametrize("i", range(100))
def test_random_niches_startkey(i):
    spec = SimSpec()
    obs = random_niches(spec, 10, "enrichment")
    assert isinstance(obs, list)
    assert "enrichment" in obs
    assert "mine" not in obs
    assert None not in obs
    assert len(obs) <= 10
    for niche in obs:
        assert niche in def_niches()

"""
def test_has_commodity():    #up_hierarchy function minimizes the error of a commodity not existing
    obs_niches = random_niches(10)
    for keyfrom, keyto in zip(obs_niches[:-1], obs_niches[1:]):
        commod = choose_commodity(keyfrom, keyto, ())
        assert commod in COMMODITIES.values() #check to see if the chosen commodity exists as a value
"""
