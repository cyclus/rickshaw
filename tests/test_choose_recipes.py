from rickshaw.generate import choose_recipes, choose_commodities, random_niches
from rickshaw.simspec import SimSpec

def test_choose_recipes():
    spec = SimSpec()
    niches = random_niches(spec, 10)
    commods = choose_commodities(spec, niches)
    assert type(commods) is list
    recipes = choose_recipes(spec, commods)
    assert type(recipes) is list
    if "mine" in niches and "enrichment" in niches:
        assert "natural_uranium" in commods
    if "natural_uranium" in commods:
        assert len(recipes) > 0

