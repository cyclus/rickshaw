{"simulation": 
    {'recipe': [{'basis': 'mass',
                 'name': 'commod_recipe',
                 'nuclide': [{'comp': int('1'), 'id': int('010010000')}]}]},
                                          
 "niche_links": {"mine": {"repository"},
                    "repository": [None]},
 "commodities": {('mine', 'repository'): 'commod_recipe'},
 "archetypes": {"mine": {":agents:Source"},
                "repository": {":agents:Sink"}}
}
