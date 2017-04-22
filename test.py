{"simulation": 
    {'recipe': [{'basis': 'mass',
                 'name': 'commod_recipe',
                 'nuclide': [{'comp': [0.5, 1.0], 'id': int('010010000')},
                            {'comp': None, 'id': int('010010000')}]}]},
                                          
 "niche_links": {"mine": {"repository"},
                    "repository": [None]},
 "commodities": {('mine', 'repository'): 'commod_recipe'},
 "archetypes": {"mine": {":agents:Source"},
                "repository": {":agents:Sink"}}
}
