from rickshaw.choose_recipes import choose_recipes 
from rickshaw.choose_commodities import choose_commodities
from rickshaw.choose_niches import random_niches

def test_choose_recipes():
    niches = random_niches(10)
    commods = choose_commodities(niches)
    assert type(commods) is list
    recipes = choose_recipes(commods)
    assert type(recipes) is list
    if "mine" in niches:
        assert "natural_uranium" in commods
    if "natural_uranium" in commods:
        assert len(recipes) > 0