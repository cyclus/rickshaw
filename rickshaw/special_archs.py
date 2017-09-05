"""Special archetypes provided as necessary to the Rickshaw input file. 
Used for fuel cycle niches that have more than just one incommodity and outcommodity.
"""
import random 

def generate_throwsink(commod, name):
    """Generic sink for outcommodities that do not become the
    incommodity of the following archetype.
    
    Parameters
    ----------
    commod : String
        Name of the commidity that the throwsink is receiving.
    name : String
        Name for the archetype in the input file.
        
    Returns
    -------
    config : Dictionary
        Dictionary formatted to represent the archetype in the input file.
    """
    vals = {}
    vals["capacity"] = 1.0e100
    vals["in_commods"] = {"val": [commod]} 
    config = {"name": name, "config": {"agents_sink": vals}}
    return config

def generate_throwsource(commod, name):
    """Generic source for commidities.
    
    Parameters
    ----------
    commod : String
        Name of the commidity that the throwsource is generating.
    name : String
        Name for the archetype in the input file.
        
    Returns
    -------
    config : Dictionary
        Dictionary formatted to represent the archetype in the input file.
    """
    vals = {}
    vals["capacity"] = 1.0e100
    vals["commod"] = commod
    vals["recipe_name"] = 'natural_uranium' 
    config = {"name": name, "config": {"agents_source": vals}}
    return config

def enrich_tails(name, vals, commod):
    """Generates a sink for the tails commodity stream. 
    
    Parameters
    ----------
    name : String
        Name for the archetype in the input file.
    vals : Dictionary
        Dictionary containing the specifications for the facilities
        in the simulation. 
    commod : String
        The commod name will be tailcommd in this case.
        
    Returns
    -------
    sink : Dictionary
        Dictionary formatted to represent the archetype in the input file.
    """
    vals[name] = 'tailcommod'
    sink = generate_throwsink('tailcommod', 'enrichsink')
    return sink

def sep_streams(name, vals, commod):
    """Generates random separation effiencies 
       for the separations facility.
    
    Parameters
    ----------
    name : String
        Name for the archetype in the input file.
    vals : Dictionary
        Dictionary containing the specifications for the facilities
        in the simulation. 
    commod : String
        Name of the commodity to be separated.
    """ 
    sep_rand = random.uniform(0.0, 1.0)
    sep = 1 - (0.0000001)**(1-sep_rand)*(0.1)**sep_rand
    nucs = ["U", "Pu"]
    streams = {"streams":{
                  "item":[{
                      "commod": commod,
                      "info": {
                         "buf_size": 1e298,
                         "efficiencies": {
                             "item": []
                         }
                      }
                  }]       
              }}
    choice = random.choice(nucs)
    if choice == "U" or choice =="Pu":
        temp = {"comp": choice, "eff": sep}
        streams["streams"]["item"][0]["info"]["efficiencies"]["item"].append(temp)
    vals[name] = streams["streams"]
    return 0

def sep_leftover(name, vals, commod):
    """Generates a sink facility for the waste
       material after separation. 
    
    Parameters
    ----------
    name : String
        Name for the archetype in the input file.
    vals : Dictionary
        Dictionary containing the specifications for the facilities
        in the simulation. 
    commod : String
        Name of the commodity to be sent to the sink.
    
    Returns
    -------
    sink: Dictionary
        Dictionary containing the specifications for a sink
        facility. 
    """
    vals[name] = 'leftovercommod'
    sink = generate_throwsink('leftovercommod', 'sepsink')
    return sink    

def ff_fill(name, vals, commod):
    """Generates a DU source facility for a fuel fabrication
        facility.  
    
    Parameters
    ----------
    name : String
        Name for the archetype in the input file.
    vals : Dictionary
        Dictionary containing the specifications for the facilities
        in the simulation. 
    commod : String
        Name of the commodity for the source.
    
    Returns
    -------
    source: Dictionary
        Dictionary containing the specifications for a source
        facility. 
    """
    vals[name] = {"val": 'fillcommod'}
    source = generate_throwsource('fillcommod', 'ffsource')
    return source

def ff_fill_recipe(name, vals, commod):
    vals[name] = "natural_uranium"
    return 0

def skip(name, vals, commod):
    return 0


def generate_region_inst(sim, sim_spec):
    """Creates a null region and inst for the randomized runs.
    This operated in-place.
    
    Parameters
    ----------
    sim : Dictionary
        Simulation specifications for the cyclus input file. 
    sim_spec : SimSpec
        The prebuild SimSpec for the simulation. 
    """
    sim["region"] = region = {
        "name": "SingleRegion",
        "config": {"NullRegion": None},
        "institution": {
            "name": "SingleInstitution",
            "initialfacilitylist": {"entry": []},
            }
        }
    entries = sim["region"]["institution"]["initialfacilitylist"]["entry"]
    if sim_spec.ni == True:
        sim['region']['institution']['config'] = {"DeployInst": generate_deploy(sim, 
                                                                      sim_spec.parameters)}
        for facility in sim["facility"]:
            if facility in sim_spec.parameters['facs']:
                continue
            else:
                entry = {"prototype": facility["name"], "number": 1}
                entries.append(entry)          
    else:
        sim['region']['institution']['config'] = {"NullInst": None}
        for facility in sim["facility"]:
            entry = {"prototype": facility["name"], "number": 1}
            entries.append(entry)
    

def generate_deploy_inst(sim):
    """This creates a deploy institution for randomized runs. 
    It will generate a number of deployment times, randomize
    the times and determine the what to deploy at those times.
    It operates in place. 

    
    Parameters
    ----------
    sim : Dictionary
        Simulation specifications for the cyclus input file. 
    """
    randtimes = sim['control']['duration']/12
    months = []
    config = {'prototypes': {'val':[]}, 'build_times': {'val': []}, 'n_build':{'val': []}, 'lifetimes': {'val':[]}}
    i = 0
    while i < randtimes:
        months.append(random.randrange(1, sim['control']['duration'], 1))
        i+=1
    months.sort()
    for date in months:
        for facility in sim["facility"]:
            config['prototypes']['val'].append(facility['name'])
            config['build_times']['val'].append(date)
            config['n_build']['val'].append(random.randint(1,10))
            config['lifetimes']['val'].append(random.randint(40, 60))
    return config
    
def trans_init_facs(sim, parameters, config):
    pstart, facpower = parameters['pstart'], parameters['facpower']
    facs, facstart, facend = parameters['facs'], parameters['facstart'], parameters['facend']
    startfacs, facnum, power = [], {},  0.0
    for fac in facs:
        i = facs.index(fac)
        if facstart[i] > 0:
            startfacs.append(i)
            facnum[i] = 0.0
    while power < pstart:
        fac = random.choice(startfacs)
        facnum[fac] += 1.0
        power += facpower[fac]
    for fac in startfacs:
        i = 0
        while i < facnum[fac]:
            config['prototypes']['val'].append(facs[fac])
            config['build_times']['val'].append(0)
            config['lifetimes']['val'].append(random.randrange(0,60,1))
            config['n_build']['val'].append(1)  
            i+=1
    return config

def generate_deploy(sim, parameters):
    """Determines the function used to build the deploy institution. 
   Parameters
    ----------
    sim : Dictionary
        Simulation specifications for the cyclus input file. 
    parameters: Dictionary
        Parameters used to define the deploy institution.
    """
    config = {}
    if 'schedule' in parameters.keys():
        config = generate_deploy_sch(sim, parameters)
    if 'lin' in parameters.keys():
        config = generate_deploy_lin(sim, parameters)
    return config

def generate_deploy_lin(sim, parameters):
    """This creates a deploy institution for randomized runs. 
    This deploy institutation is designed to test a given parameter
    space for the possibility of transition between facilities.

    Parameters
    ----------
    sim : Dictionary
        Simulation specifications for the cyclus input file. 
    parameters: Dictionary
        Parameters used to define the deploy institution.
    """
    randtimes = sim['control']['duration']/12
    months = []
    config = {'prototypes': {'val':[]}, 'build_times': {'val': []}, 'n_build':{'val': []}, 'lifetimes': {'val':[]}}
    i = 0
    facs, facstart, facend = parameters['facs'], parameters['facstart'], parameters['facend']
    try:
        gen_c = parameters['generalchance']
    except:
        print("No generalchance parameter set, using default of 10%")
        gen_c = 0.1
    deploy_c = parameters['deploychoice']    
    config = trans_init_facs(sim, parameters, config)
    while i < randtimes:
        months.append(random.randrange(1, sim['control']['duration'], 1))
        i+=1
    months.sort()
    for date in months:
        for facility in sim["facility"]:
            if facility["name"] in facs:           
                i = facs.index(facility["name"])
                if facstart[i] > date or facend[i] < date:
                    continue
                num = random.choice(deploy_c[i])
                if num == 0:
                    continue
                value, mid = 0, (date-facstart[i])/(facend[i]-facstart[i])
                if facstart[i] > 0:
                    value = mid
                else: 
                    value = 1-mid
                if random.random() < value:
                    config['prototypes']['val'].append(facility['name'])
                    config['build_times']['val'].append(date)
                    config['lifetimes']['val'].append(random.choice([40, 60]))
                    config['n_build']['val'].append(num)    
            else:
                if random.random() < gen_c:
                    config['n_build']['val'].append(1)
                    config['prototypes']['val'].append(facility['name'])
                    config['build_times']['val'].append(date)
                    config['lifetimes']['val'].append(random.choice([40, 60]))
    return config

def generate_deploy_sch(sim, parameters):
    """This creates a deploy institution for randomized runs. 
    This deploy institutation is designed to test a given parameter
    space for the possibility of transition between facilities.

    Parameters
    ----------
    sim : Dictionary
        Simulation specifications for the cyclus input file. 
    parameters: Dictionary
        Parameters used to define the deploy institution.
    """
    config = {'prototypes': {'val':[]}, 'build_times': {'val': []}, 'n_build':{'val': []}, 'lifetimes': {'val':[]}}
    sched = parameters['schedule']
    for fac, dates in sched.items():
        for date, values in dates.items():
            seed = random.random()
            i = 0
            while seed > values[i]:
                i+=1
            if i > 0:
                config['prototypes']['val'].append(fac)
                config['build_times']['val'].append(date)
                config['lifetimes']['val'].append(40)
                config['n_build']['val'].append(i)
    return config

