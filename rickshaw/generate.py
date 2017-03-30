"""Generates a random Cyclus input file."""
import os
import json
import random
import subprocess
import shutil
import special_archs as sa

from collections.abc import Sequence
from copy import deepcopy
from random import randrange
from rickshaw.lazyasd import lazyobject



T = {
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

COMMODITIES = {
    ("mine", "enrichment"): "natural_uranium",
    ("mine", "reactor:hwr"): "natural_uranium_fuel",  # in case of hwr
    ("enrichment", "fuel_fab"): "low_enriched_uranium",
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
    ("separations", "repository"): "separated_waste"
}

NUCLIDES = {'natural_uranium': [{'id': 'U235', 'comp': 0.00711},
                                {'id': 'U238', 'comp': 0.99289}],
            'low_enriched_uranium': [{'id': 'U235', 'comp': [0.03, 0.05]},
                                     {'id': 'U238', 'comp': None}],
            'low_enriched_uranium': [{'id': 'U235', 'comp': [0.03, 0.05]},
                                     {'id': 'U238', 'comp': None}],
            'used_fuel': [{'id': 'U235', 'comp': [0.00650, 0.00720]},
                          {'id': 'U238', 'comp': None},
                          {'id': 'Pu238', 'comp': [0.000235, 0.000275]},
                          {'id': 'Pu239', 'comp': [0.00535, 0.00595]},
                          {'id': 'Pu240', 'comp': [0.00249, 0.00309]},
                          {'id': 'Pu241', 'comp': [0.00150, 0.00180]},
                          {'id': 'Pu242', 'comp': [0.000812, 0.000832]},
                          {'id': 'Am241', 'comp': [0.0000545, 0.0000565]},
                          {'id': 'Am243', 'comp': [0.000166, 0.000186]},
                          {'id': 'Cm242', 'comp': [0.0000223, 0.0000243]},
                          {'id': 'Cm244', 'comp': [0.0000696, 0.0000716]}]
           }

NUCLIDES['natural_uranium_fuel'] = NUCLIDES['natural_uranium']
NUCLIDES['stored_used_fuel'] = NUCLIDES['used_uox'] = NUCLIDES['used_fuel']

DEFAULT_SOURCES = {':agents:Source', ':cycamore:Source'}
DEFAULT_SINKS = {':agents:Sink', ':cycamore:Sink'}

NICHE_ARCHETYPES = {
    "mine": {":cycamore:Source"}, #
    "conversion" : {":cycamore:Storage"}, #
    "enrichment": {":cycamore:Enrichment"},
    "fuel_fab" : {":cycamore:FuelFab"},
    "fuel_fab:uo2": {":cycamore:FuelFab"}, #not the correct archetype currently possibly
    "fuel_fab:triso": {":cycamore:FuelFab"},
    "fuel_fab:mox": {":cycamore:FuelFab"},
    "reactor": {":cycamore:Reactor"},
    "reactor:fr": {":cycamore:Reactor"},
    "reactor:lwr": {":cycamore:Reactor"},
    "reactor:hwr": {":cycamore:Reactor"},
    "reactor:htgr": {":cycamore:Reactor"},
    "reactor:rbmk": {":cycamore:Reactor"},
    "reactor:pb": {":cycamore:Reactor"},
    "storage": {":cycamore:Sink"}, #
    "storage:wet": {":cycamore:Sink"}, #
    "storage:dry": {":cycamore:Sink"}, #
    "storage:interim": {":cycamore:Sink"}, #
    "separations": {":cycamore:Separations"},
    "repository": {":cycamore:Sink"} #
    }

SPECIAL_CALLS = {(":cycamore:Enrichment", "tails_commod"): sa.enrich_tails,
    (":cycamore:Separations", "streams"): sa.sep_streams,
    (":cycamore:FuelFab", "fill_commods"): sa.ff_fill
    }

ANNOTATIONS = {}

@lazyobject
def CYCLUS_EXECUTABLE():
    return shutil.which('cyclus')


@lazyobject
def H5LS_EXECUTABLE():
    return shutil.which('h5ls')


@lazyobject
def H5_LIBPATH():
    prefix = os.path.dirname(os.path.dirname(H5LS_EXECUTABLE[:]))
    lib = os.path.join(prefix, 'lib')
    return lib


@lazyobject
def CYCLUS_LD_LIB_PATH():
    prefix = os.path.dirname(os.path.dirname(CYCLUS_EXECUTABLE[:]))
    lib = os.path.join(prefix, 'lib')
    lib += ':' + H5_LIBPATH[:]
    ld_lib_path = lib + ':' + os.environ.get('LD_LIBRARY_PATH', '')
    return ld_lib_path


@lazyobject
def CYCLUS_ENV():
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = CYCLUS_LD_LIB_PATH[:]
    return env


def random_niches(max_niches, choice="mine", niches=None):
    """Generates a randomized list of niches of the nuclear fuel cycle.
    
    Parameters
    ----------
        max_niches : int
            The maximum number of niches desired by the user, the total number
            of generated niches does not have to reach this number.
        choice : str
            If desired the starting point of the list of niches can be set. 
            Preset to the natural starting point of "mine"
        niches : None
            This will be set to be a list at the beginning of the function and
            will contain the chosen niches.
            
    Returns
    -------
        niches : list
            List of connected niches that model the steps of the full nuclear
            fuel cycle.
    """
    if niches is None:
        niches = []
    niches.append(choice)
    if max_niches == 1:
        return niches
    else:
        choice = random.sample(T[choice], 1)[0]
        if choice is None:
            return niches
        return random_niches(max_niches-1, choice, niches)

def choose_control():  
    """This program will choose the control scheme at random for a cyclus 
    input file in JSON
    
    Returns
    -------
        control : dict
            Dictionary generated to be the control scheme in the JSON cyclus
            input file
    """    
    
    duration = randrange(12, 600, 6)
    start_month = randrange(1, 12)
    start_year = randrange(2000, 2050)
    dt = randrange(2629846, 31558152, 2629846)
    
    control = {
    
                'duration' : duration,
                'startmonth' : start_month,
                'startyear' : start_year,
                'dt' : dt,
                
                }
                
    return control

def up_hierarchy(key):
    # If we have it, immediately return
    if key in COMMODITIES:
        return COMMODITIES[key]
    # If the key contains a colon, we may be able to provide a more basic form
    if ":" in key[0]:
        keyfrom, _, _ = key[0].rpartition(":")
    else:
        keyfrom = key[0]
    if ":" in key[1]:
        keyto, _, _ = key[1].rpartition(":")
    else:
        keyto = key[1]
    # If our new key is identical to the original, we can't support it
    if (keyfrom, keyto) == key:
        return None
    else:
        if (keyfrom, key[1]) != key:
            commod = up_hierarchy((keyfrom, key[1]))
            if commod is not None:
                return commod
        if (key[0], keyto) != key:
            commod = up_hierarchy((key[0], keyto))
            if commod is not None:
                return commod
        commod = up_hierarchy((keyfrom, keyto))
        return commod


def choose_commodity(keyfrom, keyto, unique_commods):
    """Determine commodity based on a from/to pairs.

    Parameters
    ----------
    keyfrom : str
        Origin niche name.
    keyto : str
        Following niche name.
    unique_commods : set
        Current names used by chosen commodities.

    Returns
    -------
    commod_name : str
        A unique commodity name.
    """
    commod = orig_commod = up_hierarchy((keyfrom, keyto))
    if commod is None:
        return None
    n = 1
    commod_name = commod
    while commod_name in unique_commods:
        commod_name = orig_commod + str(n)
        n = n + 1
    unique_commods.add(commod_name)
    return commod_name


def choose_commodities(niches):
    """Creates list of commodities individually chosen by the choose_commodity function

    Parameters
    ----------
    niches : list
        List of sequential niches returned from choose_niches.py

    Returns
    -------
    commods : list
        List of in and out commodities to be added to the archetypes in the
        input file.
    """
    commods = []
    unique_commods = set()
    for keyfrom, keyto in zip(niches[:-1], niches[1:]):
        commod = choose_commodity(keyfrom, keyto, unique_commods)
        if commod is None:
            continue
        commods.append(commod)
    return commods

def choose_recipes(commods):
    """Chooses the specific recipe for each commodity in the commods list

    Parameters
    ----------
        commods : list
            List of in and out commodities to be added to the archetypes in the
            input file.

    Returns
    -------
        recipes : list
            List of the assigned recipes to be added to the recipe section of
            the generated input file[]
    """
    recipes = []
    for commod in commods:
        recipe_dict = {}
        if commod not in NUCLIDES:
            continue
        recipe_dict['name'] = commod
        recipe_dict['basis'] = 'mass'
        nucs = recipe_dict['nuclide'] = deepcopy(NUCLIDES[commod])
        none_i = None
        total = 0.0
        u = random.uniform(0.0, 1.0)
        for i, nuc in enumerate(nucs):
            comp = nuc['comp']
            if isinstance(comp, float):
                total += comp
            elif comp is None:
                none_i = i
            elif isinstance(comp, Sequence):
                nuc['comp'] = comp = (comp[1] - comp[0])*u + comp[0]
                total += comp
        if none_i is not None:
            nucs[none_i]['comp'] = 1.0 - total
        recipes.append(recipe_dict)
    return recipes

def generate_nuclide(commod):
    pass

def choose_archetypes(niches):
    """Determines the correct archetype from cyclus or cycamore based on the niche

    Parameters
    ----------
        niches : list
            List of sequential niches returned from choose_niches.py

    Returns
    -------
        arches : list
            List of assigned archetypes. Same list length as niches.
    """
    arches = [random.choice(tuple(NICHE_ARCHETYPES[niches[0]] | DEFAULT_SOURCES))]
    for niche in niches[1:-1]:
        a = random.choice(tuple(NICHE_ARCHETYPES[niche]))
        arches.append(a)
    if len(niches) > 1:
        #used to be NICHE_ARCHETYPES[niches][-1]
        a = random.choice(tuple(NICHE_ARCHETYPES[niches[-1]] | DEFAULT_SINKS))
        arches.append(a)
    return arches

def archetype_block(arches):
    unique_arches = sorted(set(arches))
    if ':agents:Sink' not in unique_arches:
        unique_arches.append(':agents:Sink')
    if ':agents:Source' not in unique_arches:
        unique_arches.append(':agents:Source')
    if ':agents:NullInst' not in unique_arches:
        unique_arches.append(':agents:NullInst')
    if ':agents:NullRegion' not in unique_arches:
        unique_arches.append(':agents:NullRegion')
    block = {"spec" : []}
    spec_keys = ["path", "lib", "name"]
    for a in unique_arches:
        if a == ':agents:Sink':
            spec_keys.append('alias')
            a +=':agents_sink'
            spec = dict(zip(spec_keys, a.split(":")))
        if a == ':agents:Source':
            spec_keys.append('alias')
            a +=':agents_source'
            spec = dict(zip(spec_keys, a.split(":")))
        else:
            spec = dict(zip(spec_keys, a.split(":")))
        if spec["path"] == "":
            del spec["path"]
        block["spec"].append(spec)
    return block

def generate_archetype(arche, in_commod, out_commod):
    """Pulls in the metadata for each archetype

        Parameters
        ----------
            arche : str
                The name of the archetype that is being generated.
            in_commod : str
                The incommodity received by the specific archetype as
                determined by choose_commodities.py
            out_commod : str
                The outcommodity produced by the specific archetype as
                determined by choose_commodities.py

        Returns
        -------
            config : dict
                The JSON formatted archetype dictionary to be put in the input file
    """
    if arche not in ANNOTATIONS:
        anno = subprocess.check_output([CYCLUS_EXECUTABLE[:], "--agent-annotations", arche],
                                       env=CYCLUS_ENV)
        try:
            anno = json.loads(anno.decode())
        except json.decoder.JSONDecodeError:
            raise RuntimeError("JSON could not decode annotation " + anno.decode())
        ANNOTATIONS[arche] = anno
    annotations = ANNOTATIONS[arche]
    config = []
    vals = {}
    #dereference aliases
    for name, var in list(annotations["vars"].items()):
        if isinstance(var, str):
            annotations["vars"][name] = annotations["vars"].pop(var)
    #fill in and randomly generate state variables        
    for name, var in annotations["vars"].items():
        if (arche, name) in SPECIAL_CALLS:
            temp = SPECIAL_CALLS[(arche, name)](name, vals, out_commod)
            if temp != 0:
                config.append(temp)
            continue
        uitype = var.get("uitype", None)
        var_type = var["type"]
        if uitype == "range":
            if "nichedomain" in var:
                rng = var["nichedomain"].get(niche, var["range"])
            else:
                rng = var["range"]
            val = random.uniform(*rng)
            vals[name] = val
        elif uitype == "incommodity":
            vals[name] = in_commod
        elif uitype == ["oneormore", "incommodity"]:
            vals[name] = [in_commod]
        elif uitype == "outcommodity":
            vals[name] = out_commod
        elif uitype == ["oneormore", "outcommodity"]:
            vals[name] = [out_commod]
        elif uitype == "commodity" or uitype == ["oneormore", "commodity"]:
            raise KeyError("Can't generate to commodity please use incommodity "
                           "or outcommodity")
        elif var_type == "double" or var_type == "float":
            vals[name] = var.get("default", 0.0)
        elif var_type == "int":
            vals[name] = var.get("default", 0)
    alias = arche.rpartition(":")[-1]
    if arche == ':agents:Sink':
        alias = 'agents_sink'
    if arche == ':agents:Source':
        alias = 'agents_source'
    config.append({"name": alias, "config": {alias: vals}})
    return config

def generate_reg_inst():
    """Creates a null region and inst for the randomized runs.
        
    Parameters
    ----------
    
    Returns
    -------
    
    """ 

def generate(max_num_niches=10):
    """Creates a random Cyclus simulation input file dict.

    Parameters
    ----------
    max_num_niches : int, optional
        The maximum number of niches in the simulation

    Returns
    -------
    inp : dict
        A simulation dictionary in JSON form, suitable for use
        as a Cyclus input file.
    """
    # intial structure
    inp = {"simulation": {}}
    sim = inp["simulation"]
    sim["control"] = choose_control()
    # choose niches and archtypes
    niches = random_niches(max_niches=max_num_niches)
    arches = choose_archetypes(niches)
    commods = choose_commodities(niches)
    recipes = choose_recipes(commods)
    if len(recipes) == 1:
        recipes = recipes[0]
    sim["archetypes"] = archetype_block(arches)
    #put the other things in here
    sim["recipe"] = recipes
    protos = {}
    protos[arches[0]] = generate_archetype(arches[0], None, commods[0])[0]
    for arche, in_commod, out_commod in zip(arches[1:-1], commods[:-1], commods[1:]):
        temp_arch = generate_archetype(arche, in_commod, out_commod)
        for arch in temp_arch:
            protos[arch["name"]] = arch

    protos[arches[-1]] = generate_archetype(arches[-1], commods[-1], None)[0]
    sim["facility"] = list(protos.values())
    return inp

