{'simulation': 
    {'recipe': [{'basis': 'mass',
                 'name': 'commod_recipe',
                 'nuclide': [{'comp': [0.95, 1.0], 'id': int('922350000')},
                            {'comp': None, 'id': int('922380000')}]}],
    'facility': [
                {
                    "config": {
                        "testfac": {
                            "testpyjinja": "pyjinja:{%set list=['u', 'pu']%}{% set test=[] %}{% for item in list %}{% set _= test.append({item : 0.9|uniform(0.99)}) %}{% endfor %}{{test}}",
                            "testjsonjinja": "jsonjinja:{%set list=[\"u\", \"pu\"]%}{% set test=[] %}{% for item in list %}{% set _= test.append(item) %}{% endfor %}{{test}}",
                            "testpy": "py:{\"u\":0.99, \"pu\": uniform(0.9, 0.99)}",
                            "testjson": "json:{\"u\": 0.99, \"pu\": 0.999, \"cm\": 0.9}",
                        }
                    },
                    "name": "testfac",
                    "spec": ":agent:test"
                }]},                            
 "niche_links": {"mine" : {"reactor:hwr"},
                 "reactor:hwr" : {"repository"},
                 "repository" : {None}}
}
