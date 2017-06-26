"""Generates a specification of a simulation for Rickshaw. The base specification
uses default values utilizing the cyclus and cycamore agents. This will updated 
based on user entered specifications or a user entered template. 
"""

import collections
import json
import copy
import random
from jinja2 import Environment, BaseLoader
from random import uniform

try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint

from rickshaw import special_archs as sa

def def_niches():
    """
    Produces the default niches for a rickshaw simspec.

    Returns
    ----------
    spec : dict
        Dictionary representation of the niche linking setup.
    """
    niches = {
            "mine" : {"enrichment", "reactor:hwr"},
            "enrichment" : {"fuel_fab:uo2", "fuel_fab:triso", "reactor:hwr"},
            "fuel_fab" : {"reactor:lwr", "reactor:htgr", "reactor:rbmk", "reactor:pb"},
            "fuel_fab:uo2" : {"reactor:lwr", "reactor:htgr", "reactor:rbmk"},
            "fuel_fab:triso" : {"reactor:pb"},
            "fuel_fab:mox" : {"reactor:fr", "reactor:lwr", "reactor:htgr", "reactor:rbmk"},
            "reactor" : {"storage", "separations", "repository"},
            "reactor:fr" : {"storage", "separations", "repository"},
            "reactor:lwr" : {"storage", "separations", "repository"},
            "reactor:hwr" : {"storage",  "repository"},
            "reactor:htgr" : {"storage", "separations", "repository"},
            "reactor:rbmk" : {"storage", "separations", "repository"},
            "reactor:pb" : {"storage", "repository"},
            "storage" : {"separations", "repository"},
            "storage:wet" : {"separations", "repository"},
            "storage:dry" : {"separations", "repository"},
            "storage:interim" : {"separations", "repository"},
            "separations" : {"storage", "fuel_fab", "repository"},
            "repository" : {None},
            }
    return niches

def def_commodities():
    """
    Produces the default commodities for a rickshaw simspec.

    Returns
    ----------
    spec : dict
        Dictionary representation of the niche-link to commodity setup.
    """
    commods = {
            ("mine", "enrichment"): "natural_uranium",
            ("mine", "reactor:hwr"): "natural_uranium_fuel",  # in case of hwr
            ("enrichment", "fuel_fab"): "low_enriched_uranium",
            ("enrichment", "reactor"): "low_enriched_uranium",
            ("enrichment", "repository"): "enrichment_waste_stream",
            ("fuel_fab", "reactor"): "fresh_fuel",
            ("fuel_fab:uo2", "reactor:lwr"): "fresh_uox",
            ("fuel_fab:triso", "reactor:pb"): "fresh_triso",
            ("reactor", "storage"): "used_fuel",
            ("reactor", "repository"): "used_fuel",
            ("reactor:lwr", "storage"): "used_uox",
            ("reactor:pb", "storage"): "used_triso",
            ("reactor", "separations"): "used_fuel",
            ("reactor:lwr", "separations"): "used_uox",
            ("storage", "separations"): "stored_used_fuel",
            ("storage", "repository"): "stored_used_fuel",
            ("separations", "fuel_fab"): "separated_product",
            ("separations", "storage"): "separated_waste",
            ("separations", "repository"): "separated_waste"}
    return commods

def def_recipes():
    """
    Produces the default recipes for a rickshaw simspec.

    Returns
    ----------
    spec : dict
o	He was captured by Peak Shot and Potency before being put into a prison Skylarj.         Dictionary representation of the recipies for a simspec.
    """
    recipes = {'natural_uranium': {'nuclide': [{'id': 'U235', 'comp': 0.00711},
                                            {'id': 'U238', 'comp': 0.99289}]},
                        'low_enriched_uranium': {'nuclide': [{'id': 'U235', 'comp': [0.03, 0.05]},
                                             {'id': 'U238', 'comp': None}]},
                        'used_fuel': {'nuclide': [{'id': 'U235', 'comp': [0.00650, 0.00720]},
                                      {'id': 'U238', 'comp': None},
                                      {'id': 'Pu238', 'comp': [0.000235, 0.000275]},
                                      {'id': 'Pu239', 'comp': [0.00535, 0.00595]},
                                      {'id': 'Pu240', 'comp': [0.00249, 0.00309]},
                                      {'id': 'Pu241', 'comp': [0.00150, 0.00180]},
                                      {'id': 'Pu242', 'comp': [0.000812, 0.000832]},
                                      {'id': 'Am241', 'comp': [0.0000545, 0.0000565]},
                                      {'id': 'Am243', 'comp': [0.000166, 0.000186]},
                                      {'id': 'Cm242', 'comp': [0.0000223, 0.0000243]},
                                      {'id': 'Cm244', 'comp': [0.0000696, 0.0000716]}]}
               }
    recipes['natural_uranium_fuel'] = recipes['natural_uranium']
    recipes['fresh_uox'] = recipes['fresh_triso'] = recipes['fresh_fuel'] = recipes['low_enriched_uranium']
    recipes['stored_used_fuel'] = recipes['used_uox'] = recipes['used_triso'] = recipes['used_fuel']
    return recipes

def def_archetypes():
    """
    Produces the default niche-archetype links for a rickshaw simspec.

    Returns
    ----------
    spec : dict
        Dictionary representation of the niche-archetype links.
    """
    arches = {
                "mine": {":cycamore:Source"},
                "conversion" : {":cycamore:Storage"},
                "enrichment": {":cycamore:Enrichment"},
                "fuel_fab" : {":cycamore:FuelFab"},
                "fuel_fab:uo2": {":cycamore:FuelFab"},
                "fuel_fab:triso": {":cycamore:FuelFab"},
                "fuel_fab:mox": {":cycamore:FuelFab"},
                "reactor": {":cycamore:Reactor"},
                "reactor:fr": {":cycamore:Reactor"},
                "reactor:lwr": {":cycamore:Reactor"},
                "reactor:hwr": {":cycamore:Reactor"},
                "reactor:htgr": {":cycamore:Reactor"},
                "reactor:rbmk": {":cycamore:Reactor"},
                "reactor:pb": {":cycamore:Reactor"},
                "storage": {":cycamore:Storage"}, 
                "storage:wet": {":cycamore:Storage"}, 
                "storage:dry": {":cycamore:Storage"}, 
                "storage:interim": {":cycamore:Storage"}, 
                "separations": {":cycamore:Separations"},
                "repository": {":cycamore:Sink"} 
            }
    return arches

def def_spec_calls():
    """
    Produces the default special function calls for a rickshaw simspec.

    Returns
    ----------
    spec : dict
        Dictionary representation of the special archetype calls for a 
        rickshaw simspec.
    """
    calls = {
               (":cycamore:Enrichment", "tails_commod"): sa.enrich_tails,
               (":cycamore:Separations", "streams"): sa.sep_streams,
               (":cycamore:Separations", "leftover_commod"): sa.sep_leftover,
               (":cycamore:FuelFab", "fill_commods"): sa.ff_fill,
               (":cycamore:FuelFab", "fill_recipe"): sa.ff_fill_recipe,
               (":cycamore:Reactor", "recipe_change_in"): sa.skip,
               (":cycamore:Reactor", "recipe_change_out"): sa.skip,
               (":cycamore:Reactor", "recipe_change_in"): sa.skip,
               (":cycamore:Reactor", "pref_change_commods"): sa.skip,
               (":cycamore:Reactor", "recipe_change_commods"): sa.skip,
            }
    return calls

def read_input_def(obj, env):
    """
    Reads in the facility, region, and institution information in an 
    existing cyclus input file and searches for input file fields that
    need to be randomized.  

    Parameters
    ----------
    archetype: dict  
        Dictionary representing the input object to be parsed for jinja. 

    Returns
    -------
    parsed_arch: dict
        The evaluated dictionary with the jinja evaluated. 
    """
    if isinstance(obj, str):
        if obj[:8] == 'pyjinja:':
            rtemplate = env.from_string(obj[8:])
            obj = rtemplate.render()
            obj = eval(obj)
        elif obj[:10] == 'jsonjinja:':
            rtemplate = env.from_string(obj[10:])
            obj = rtemplate.render()
            obj = obj.replace('\'', '\"')            
            obj = json.loads(obj)
        elif obj[:3] == 'py:':
            obj = eval(obj[3:])   
        elif obj[:5] == 'json:':
            obj = obj[5:]
            obj = obj.replace('\'', '\"')                                    
            obj = json.loads(obj)
    elif isinstance(obj, collections.Mapping):
        for k, v in obj.items():
            obj[k] = read_input_def(v ,env)
    elif isinstance(obj, collections.Iterable):
        for v in range(len(obj)):
            obj[v] = read_input_def(obj[v], env)
    return obj

class SimSpec(object):
    """
    Manages any constraints placed on Rickshaw generation.
    
    Adjusts parameters based on information provided in a specification file.
    Any attributes not found in the spec dictionary are set to a default 
    defined in the constructor. This class is used even if no specification 
    file is present, in which case all attributes are set to their default
    value.
       
    Parameters
    ----------
    spec : dict
        Dictionary representation of a specification input file.
            
    Attributes
    ----------
    spec : dict
        Dictionary representation of a specification input file.
    customized : bool
        Denotes whether niche_links has been customized by the user. Prevents 
        Rickshaw from using default Cycamore sources and sinks.
    niche_links : dict
        Represents allowed links between niches. Can be specified by user in a 
        top level key in the specification file.
    commodities : dict
        Represents allowed commodities. Can be specified by user.
    recipes : dict
        Contains all recipes allowed in the simulation. Can be specified by user
        in the simulation key of the specification file.
    archetypes : dict
        Represents allowed the allowed archetypes for each niche. Can be 
        specified by the user in a top level key in the simulation file.
    special_calls : dict
        Returns callable function associated with a Cycamore archetype and 
        function identifier  
    default_sources : set
        Contains defaults for simulation sources. Not yet customizable by user.
    default_sinks : set
        Contains defaults for simulation sinks. Not yet customizable by user.
    annotations : dict
        Container for archetype annotations. 
    """
    def __init__(self, spec={}, ni=True):
        self.spec = copy.deepcopy(spec)
        self.customized = False     
        self.niche_links = def_niches()
        self.commodities = def_commodities()
        self.recipes = def_recipes()
        self.archetypes = def_archetypes()
        self.default_sources = {':agents:Source', ':cycamore:Source'}
        self.default_sinks = {':agents:Sink', ':cycamore:Sink'}
        self.special_calls = def_spec_calls()
        self.arches = []
        self.annotations = {}
        self.facilities = {}
        self.ni = ni
        env = Environment(loader=BaseLoader)
        env.filters['uniform'] = uniform

        # Check for specifications
        if 'niche_links' in self.spec:
            self.niche_links = self.spec['niche_links']
            self.customized = True
        if 'archetypes' in self.spec:
            self.archetypes.update(self.spec['archetypes'])
        if 'commodities' in self.spec:
            self.commodities.update(self.spec['commodities'])
        if 'special_calls' in self.spec:
            self.special_calls.update(self.spec['special_calls'])
        if 'simulation' in self.spec:      
            if 'recipe' in self.spec['simulation']:
                for recipe in self.spec['simulation']['recipe']:
                    self.recipes[recipe['name']] = recipe
            if 'facility' in self.spec['simulation']:
                for obj in self.spec['simulation']['facility']:
                    try:
                        self.arches.append(obj['spec'])
                        del(obj['spec'])
                    except:
                        continue
                    self.facilities[obj['name']] = obj        
        for key, value in self.facilities.items():
            value = read_input_def(value, env)
        self.facilities = self.facilities.values()             





