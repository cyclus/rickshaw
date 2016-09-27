# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:49:39 2016

@author: adam
"""
import pytest


from niches import random_niches, T

@pytest.mark.parametrize("i", range(100))
def test_random_niches(i):
    obs = random_niches(10)
    assert isinstance(obs, set)
    assert "mine" in obs
    assert None not in obs
    assert len(obs) <= 10
    for niche in obs:
        assert niche in T
        
@pytest.mark.parametrize("i", range(100))
def test_random_niches_startkey(i):
    obs = random_niches(10, "enrichment")
    assert isinstance(obs, set)
    assert "enrichment" in obs
    assert "mine" not in obs
    assert None not in obs
    assert len(obs) <= 10
    for niche in obs:
        assert niche in T