# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:49:39 2016

@author: adam
"""
import pytest
from rickshaw.simspec import SimSpec
from rickshaw.generate import up_hierarchy, choose_commodity, choose_commodities

@pytest.mark.parametrize("key, expected", [
    [("mine", "enrichment"), "natural_uranium"],
    [("mine:uranium", "enrichment"), "natural_uranium"],
    [("mine", "enrichment:uranium"), "natural_uranium"],
    [("mine:uranium", "enrichment:uranium"), "natural_uranium"],
    [("reactor:lwr", "separations"), "used_uox"],
    [("fuel_fab:triso", "reactor:pb"), "fresh_triso"],
    [("fuel_fab", "reactor:lwr"), "fresh_fuel"],
])
def test_up_hierarchy(key, expected):
    spec = SimSpec()
    observed = up_hierarchy(spec, key)
    assert expected == observed


@pytest.mark.parametrize("keyfrom, keyto, expected", [
    ("mine", "enrichment", "natural_uranium"),
    ("mine", "reactor:hwr", "natural_uranium_fuel"),
])
def test_choose_commodity(keyfrom, keyto, expected):
    spec = SimSpec()
    unique_commods = set()
    observed = choose_commodity(spec, keyfrom, keyto, unique_commods)
    assert expected == observed


@pytest.mark.parametrize("niches, expected", [
    [["mine", "enrichment", "fuel_fab", "reactor:lwr", "storage", "separations",
      "storage", "repository"],
      ["natural_uranium", "low_enriched_uranium", "fresh_fuel", "used_uox", "stored_used_fuel",
       "separated_waste", "stored_used_fuel1"]],
    [["storage", "separations", "storage", "separations", "storage", "repository"],
     ["stored_used_fuel", "separated_waste", "stored_used_fuel1", "separated_waste1",
      "stored_used_fuel2"]],
    [["mine", "reactor:hwr", "repository"],
     ["natural_uranium_fuel", "used_fuel"]],
])
def test_choose_commodities(niches, expected):
    spec = SimSpec()
    observed = choose_commodities(spec, niches)
    assert expected == observed

