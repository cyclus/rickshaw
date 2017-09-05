{
'simulation': 
    {
    'facility': [
                {
                    "config": {
                        "Reactor": {
                            "fuel_outrecipes": {
                                "val": [
                                    "used_fuel"
                                ]
                            },
                            "cycle_step": 0,
                            "fuel_incommods": {
                                "val": [
                                    "natural_uranium_fuel"
                                ]
                            },
                            "cycle_time": 18,
                            "assem_size": 14284.505461890136,
                            "fuel_outcommods": {
                                "val": [
                                    "used_fuel"
                                ]
                            },
                            "n_assem_batch": 0,
                            "n_assem_spent": 452793041,
                            "fuel_inrecipes": {
                                "val": [
                                    "natural_uranium_fuel"
                                ]
                            },
                            "refuel_time": 1,
                            "n_assem_core": 2,
                            "power_cap": 800,
                            "n_assem_fresh": 2
                        }
                    },
                    "name": "Reactor",
                    "spec": ":cycamore:Reactor"
                },
                {
                    "config": {
                        "Reactor": {
                            "fuel_outrecipes": {
                                "val": [
                                    "used_fuel"
                                ]
                            },
                            "cycle_step": 0,
                            "fuel_incommods": {
                                "val": [
                                    "natural_uranium_fuel"
                                ]
                            },
                            "cycle_time": 18,
                            "assem_size": 14284.505461890136,
                            "fuel_outcommods": {
                                "val": [
                                    "used_fuel"
                                ]
                            },
                            "n_assem_batch": 0,
                            "n_assem_spent": 452793041,
                            "fuel_inrecipes": {
                                "val": [
                                    "natural_uranium_fuel"
                                ]
                            },
                            "refuel_time": 1,
                            "n_assem_core": 2,
                            "power_cap": 600,
                            "n_assem_fresh": 2
                        }
                    },
                    "name": "Reactor1",
                    "spec": ":cycamore:Reactor"
                }
                ]
    },
    "niche_links": {"mine" : {"reactor:hwr"},
                 "reactor:hwr" : {"reactor:fr"},
                 "reactor:fr": {"repository"},
                 "repository" : {None}
    },
    #"parameters": {"facs": ["Reactor", "Reactor1"], "facpower": [800.0, 600.0],"facstart": [0, 300], "facend": [300, 2000], "deploychoice": [[0,1,2],[2 ,3,4]], "pstart": 5000, "rate": 0.02, "generalchance": 0.1}
    "parameters": {"schedule": {"Reactor": {20: [0.0, 0.4, 0.8, 1.0], 40: [0.0, 0.0, 0.0, 1.0]}}, "facs": ['Reactor', 'Reactor1'], "pstart": 5000, "rate": 0.02}
}
