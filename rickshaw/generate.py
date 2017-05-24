"""Generates a random Cyclus input file. Contains functions to stochastically
generate a niche path through the nuclear fuel cycle as well as the appropriate
archetypes, recipes, commodities, and a control scheme for the nuclear fuel cycle
those niches represent. Archetypes state variables with a "range" uitype are
stochastically generated within a physically valid range.
"""
import os
import json
import random
import subprocess
import shutil
import logging
from collections.abc import Sequence
from copy import deepcopy
from random import randrange, choice

try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint
from rickshaw import simspec
from rickshaw import special_archs as sa
from rickshaw.lazyasd import lazyobject

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


def random_niches(sim_spec, max_niches, choice="mine", niches=None):
    """Generates a randomized list of niches of the nuclear fuel cycle.

    Parameters
    ----------
        sim_spec : SimSpec
            Specification for simulation generation
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
    logging.info('Starting Niches')
    if niches is None:
        niches = []
    niches.append(choice)
    if max_niches == 1:
        logging.info('Finishing Niches')
        return niches
    else:
        choice = random.sample(sim_spec.niche_links[choice], 1)[0]
        if choice is None:
            logging.info('Finishing Niches')
            return niches
        logging.info('Finishing Niches')
        return random_niches(sim_spec, max_niches-1, choice, niches)

def choose_control():
    """This program will choose the control scheme at random for a cyclus
    input file in JSON

    Returns
    -------
        control : dict
            Dictionary generated to be the control scheme in the JSON cyclus
            input file
    """
    logging.info('starting control')   
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
    logging.info('finishing control')
    return control

def up_hierarchy(sim_spec, key):
    logging.info('start upheir')
    # If we have it, immediately return
    if key in sim_spec.commodities:
        return sim_spec.commodities[key]
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
        logging.info('end upheir')    
        return None
    else:
        if (keyfrom, key[1]) != key:
            commod = up_hierarchy(sim_spec, (keyfrom, key[1]))
            if commod is not None:
                logging.info('end upheir')
                return commod
        if (key[0], keyto) != key:
            commod = up_hierarchy(sim_spec, (key[0], keyto))
            if commod is not None:
                logging.info('end upheir')
                return commod
        commod = up_hierarchy(sim_spec, (keyfrom, keyto))
        logging.info('end upheir')
        return commod


def choose_commodity(sim_spec, keyfrom, keyto, unique_commods):
    """Determine commodity based on a from/to pairs.

    Parameters
    ----------
    sim_spec : SimSpec
            Specification for simulation generation
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
    logging.info('commod')
    commod = orig_commod = up_hierarchy(sim_spec, (keyfrom, keyto))
    if commod is None:
        logging.info('commod is none, end commod')
        return None
    n = 1
    commod_name = commod
    while commod_name in unique_commods:
        commod_name = orig_commod + str(n)
        n = n + 1
    unique_commods.add(commod_name)
    logging.info('end commod')
    return commod_name


def choose_commodities(sim_spec, niches):
    """Creates list of commodities individually chosen by the choose_commodity function

    Parameters
    ----------
    sim_spec : SimSpec
            Specification for simulation generation
    niches : list
        List of sequential niches returned from choose_niches.py

    Returns
    -------
    commods : list
        List of in and out commodities to be added to the archetypes in the
        input file.
    """
    logging.info('start choose commodities')
    commods = []
    unique_commods = set()
    for keyfrom, keyto in zip(niches[:-1], niches[1:]):
        commod = choose_commodity(sim_spec, keyfrom, keyto, unique_commods)
        if commod is None:
            continue
        commods.append(commod)
    logging.info('end choose commodities')
    return commods

def choose_recipes(sim_spec, commods):
    """Chooses the specific recipe for each commodity in the commods list

    Parameters
    ----------
        sim_spec : SimSpec
            Specification for simulation generation
        commods : list
            List of in and out commodities to be added to the archetypes in the
            input file.

    Returns
    -------
        recipes : list
            List of the assigned recipes to be added to the recipe section of
            the generated input file[]
    """
    logging.info('start choose recipes')
    recipes = []
    for commod in commods:
        recipe_dict = {}
        if commod not in sim_spec.recipes:
            recipes.append(None)
            continue
        recipe_dict['name'] = commod
        recipe_dict['basis'] = 'mass'
        nucs = recipe_dict['nuclide'] = deepcopy(sim_spec.recipes[commod]['nuclide'])
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
    logging.info('end recipes')
    return recipes

def generate_nuclide(commod):
    pass

def choose_archetypes(sim_spec, niches):
    """Determines the correct archetype from cyclus or cycamore based on the niche

    Parameters
    ----------

    sim_spec : SimSpec
        Specification for simulation generation
    niches : list
        List of sequential niches returned from choose_niches.py


    Returns
    -------
    arches : list
        List of assigned archetypes. Same list length as niches.
    """
    logging.info('start choose arch')
    if sim_spec.customized:
        arches = [random.choice(tuple(sim_spec.archetypes[niches[0]]))]
    else:
        arches = [random.choice(tuple(sim_spec.archetypes[niches[0]] | sim_spec.default_sources))]
    for niche in niches[1:-1]:
        a = random.choice(tuple(sim_spec.archetypes[niche]))
        arches.append(a)
    if len(niches) > 1:
        #used to be NICHE_ARCHETYPES[niches][-1]
        if sim_spec.customized:
            a = random.choice(tuple(sim_spec.archetypes[niches[-1]]))
        else:
            a = random.choice(tuple(sim_spec.archetypes[niches[-1]] | sim_spec.default_sinks))
        arches.append(a)
    logging.info('end choose arch')    
    return arches

def archetype_block(sim_spec, arches):
    """Formats the archetypes into the input file format

    Parameters
    ----------
    arches : list
        List of assigned archetype.

    Returns
    -------
    block : dictionary
        Dictionary containing each necessary element of the archetype
        block in a Cyclus input file.
    """
    logging.info('start arch block')
    arches = sim_spec.arches + arches
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
    logging.info('end arch block')
    return block

def generate_archetype(sim_spec, arche, in_commod, out_commod, in_recipe, out_recipe):
    """Pulls in the metadata for each archetype


    Parameters
    ----------
        sim_spec : SimSpec
            Specification for simulation generation
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
    logging.info('start generate arch')
    if arche not in sim_spec.annotations:
        anno = subprocess.check_output([CYCLUS_EXECUTABLE[:], "--agent-annotations", arche],
                                       env=CYCLUS_ENV)
        try:
            anno = json.loads(anno.decode())
        except json.decoder.JSONDecodeError:
            raise RuntimeError("JSON could not decode annotation " + anno.decode())
        sim_spec.annotations[arche] = anno
    annotations = sim_spec.annotations[arche]
    config = []
    vals = {}
    #dereference aliases
    for name, var in list(annotations["vars"].items()):
        if isinstance(var, str):
            annotations["vars"][name] = annotations["vars"].pop(var)
    #fill in and randomly generate state variables
    for name, var in annotations["vars"].items():
        if (arche, name) in sim_spec.special_calls:
            temp = sim_spec.special_calls[(arche, name)](name, vals, out_commod)
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
            if var_type == "int":
                val = int(val)
            vals[name] = val
        elif uitype == "combobox":
            vals[name] = choice(var["categorical"])
        elif uitype == "incommodity":
            vals[name] = in_commod
        elif uitype == ["oneormore", "incommodity"]:
            vals[name] = {"val" : [in_commod]}
        elif uitype == "outcommodity":
            vals[name] = out_commod
        elif uitype == ["oneormore", "outcommodity"]:
            vals[name] = {"val" : [out_commod]}
        elif uitype == "commodity" or uitype == ["oneormore", "commodity"]:
            raise KeyError("Can't generate to commodity please use incommodity "
                           "or outcommodity")
        elif uitype == "inrecipe" and "default" not in var:
            vals[name] = in_recipe["name"]
        elif uitype == ["oneormore", "inrecipe"] and "default" not in var:
            vals[name] = {"val" : [in_recipe["name"]]}
        elif uitype == "outrecipe" and "default" not in var:
            vals[name] = out_recipe["name"]
        elif uitype == ["oneormore", "outrecipe"] and "default" not in var:
            vals[name] = {"val" : [out_recipe["name"]]}
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
    logging.info('end generate arch')
    return config


def generate_region_inst(sim):
    """Creates a null region and inst for the randomized runs.
    This operated in-place.
    """
    logging.info('region')
    sim["region"] = region = {
        "name": "SingleRegion",
        "config": {"NullRegion": None},
        "institution": {
            "name": "SingleInstitution",
            "config": {"NullInst": None},
            "initialfacilitylist": {"entry": []},
            }
        }
    entries = sim["region"]["institution"]["initialfacilitylist"]["entry"]
    for facility in sim["facility"]:
        entry = {"prototype": facility["name"], "number": 1}
        entries.append(entry)
    logging.info('end region')

def generate(max_num_niches=10, sim_spec=None):
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
    logging.info('generate start')
    inp = {"simulation": {}}
    sim = inp["simulation"]
    sim["control"] = choose_control()
    # choose niches and archtypes
    niches = random_niches(sim_spec, max_niches=max_num_niches)
    arches = choose_archetypes(sim_spec, niches)
    commods = choose_commodities(sim_spec, niches)
    recipes = choose_recipes(sim_spec, commods)
    sim["archetypes"] = archetype_block(sim_spec, arches)
    #put the other things in here
    sim["recipe"] = [r for r in recipes if r is not None]
    protos = {}
    protos[arches[0]] = generate_archetype(sim_spec, arches[0], None, commods[0], None, recipes[0])[0]
    for arche, in_commod, out_commod, in_recipe, out_recipe in zip(arches[1:-1],
                                            commods[:-1], commods[1:],
                                            recipes[:-1], recipes[1:]):       
        if arche in sim_spec.arches:
            continue
        temp_arch = generate_archetype(sim_spec, arche, in_commod, out_commod, in_recipe, out_recipe)
        for arch in temp_arch:
            base_name = arch["name"]
            i = 1
            while arch["name"] in protos:
                arch["name"] = base_name + str(i)
                i+=1
            protos[arch["name"]] = arch
    protos[arches[-1]] = generate_archetype(sim_spec, arches[-1], commods[-1], None, None, None)[0]
    sim["facility"] = list(protos.values())
    sim["facility"] += sim_spec.facilities
    generate_region_inst(sim)
    logging.info('generate end')
    return inp

