{
    'simulation': {},
    'niche_links': {"mine": {"reactor:hwr", "reactor:lwr"}, 
                "reactor:hwr": {"repository"} ,
                "reactor:lwr":{"repository"},
                "repository": {None}
     },
    'archetypes': {"mine": {":cycamore:Source"},
                  "reactor:hwr": {":cycamore:Reactor"},
                  "reactor:lwr": {":cycamore:Reactor"},
                  "repository": {":cycamore:Sink"}
                 }
}
