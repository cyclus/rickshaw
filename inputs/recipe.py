{'simulation': 
    {'recipe': [{
                "basis": "mass",
                "name": "stored_used_fuel",
                "nuclide": [
                    {
                        "comp": "py:random.uniform(0.006,0.007)",
                        "id": "U235"
                    },
                    {
                        "comp": None,
                        "id": "U238"
                    },
                    {
                        "comp": "py:random.uniform(0.0002, 0.0003)",
                        "id": "Pu238"
                    },
                    {
                        "comp": "py:random.uniform(0.005, 0.006)",
                        "id": "Pu239"
                    },
                    {
                        "comp": "py:random.uniform(0.002, 0.003)",
                        "id": "Pu240"
                    },
                    {
                        "comp": "py:random.uniform(0.001, 0.002)",
                        "id": "Pu241"
                    },
                    {
                        "comp": "py:random.uniform(0.008, 0.009)",
                        "id": "Pu242"
                    },
                    {
                        "comp": "py:random.uniform(5.e-5, 6.e-5)",
                        "id": "Am241"
                    },
                    {
                        "comp": "py:random.uniform(0.0001, 0.0002)",
                        "id": "Am243"
                    },
                    {
                        "comp": "py:random.uniform(2.e-5, 3.e-5)",
                        "id": "Cm242"
                    },
                    {
                        "comp": "py:random.uniform(7.e-5, 8.e-5)",
                        "id": "Cm244"
                    }]
    }]},
"niche_links": {"mine" : {"reactor:hwr"},
                 "reactor:hwr" : {"repository"},
                 "repository" : {None}}
}
