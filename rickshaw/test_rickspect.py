{
    'simulation': {},
    'niche_links': {"mine": {"enrichment"}, 
                "enrichment": {"fuel_fab:uo2", "reactor:hwr"}, 
                "fuel_fab:uo2": {"reactor:lwr"}, 
                "reactor:hwr": {"repository"} ,
                "reactor:lwr":{"repository"}
              },
    'archetypes': {"mine": {":cycamore:Source"},
                  "enrichment": {":cycamore:Enrichment"},
                  "fuel_fab:uo2": {":cycamore:FuelFab"},
                  "reactor:hwr": {":cycamore:Reactor"},
                  "reactor:lwr": {":cycamore:Reactor"},
                  "repository": {":cycamore:Sink"}
                 }
}
