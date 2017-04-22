Rickshaw Tutorial
=================
You can get started using Rickshaw by following these steps:

1. Clone the Git repo
2. Run the installation script
3. Write a specification file (optional)

Rickshaw Dependencies
---------------------
First, make sure you have the following dependencies installed for Rickshaw to work correctly.

- Cyclus
- Cycamore
- websockets
- DockerPy
- sphinx*
- cloud_sptheme*
- numpydoc*

\* *for building documentation*


1. Cloning the Repo
-------------------
Run the following from the command line:

``git clone https://github.com/ergs/rickshaw.git``

2. Installing Rickshaw
----------------------
From the top-level ``rickshaw`` directory, run ``python setup.py install``

3. Writing a Specification File (optional)
------------------------------------------
Specification files are Rickshaw input files in which you can define constraints 
for generation. For instance, you have the ability to restrict Rickshaw to a subset 
of Archetypes, Niches, Recipes, etc.

A specification file can be in either JSON or Python format.

Here's an example:

.. code-block:: python

  # test_specification_input.py
  {
      # Simulation data definitions
      'simulation': {'recipe': [{'basis': 'mass',
                                 'name': 'commod_recipe',
                                 'nuclide': [{'comp': [0.5, 1.0], 'id': int('010010000')},
                                             {'comp': None, 'id': int('010010000')}]
                               }]
                    },
      # Desired niches for Rickshaw to use
      'niche_links': {"mine": {"reactor:hwr", "reactor:lwr"}, 
                      "reactor:hwr": {"repository"} ,
                      "reactor:lwr":{"repository"},
                      "repository": {None}
                     },
      # Disired archetypes which fit desired niches
      'archetypes': {"mine": {":cycamore:Source"},
                     "reactor:hwr": {":cycamore:Reactor"},
                     "reactor:lwr": {":cycamore:Reactor"},
                     "repository": {":cycamore:Sink"}
                    }
  }

Any of the following may be specified as top-level keys in your file:

- ``niche_links``
- ``archetypes``
- ``commodities``

The above define the allowed structure of a Rickshaw-generated input file.

You'll also notice the top-level ``simulation`` key in the specification file.
This is where you can define literal data or data ranges for generated simulations.
At this time, only the ``recipe`` block placed here is read by Rickshaw.

Running Rickshaw
----------------
After following the steps above, you can run Rickshaw via the ``rickshaw`` command from the command line.
With no flags or options set, Rickshaw will produce one output file with no constraining specification.

- To specify the number of input files to generate, use ``rickshaw -n [number of runs]``. 
  Each file will be saved in the format ``x.json`` where ``x`` is in the range [0, n-1].

- To load a specification file, use ``rickshaw -i [file_name]``

- To run Rickshaw in verbose mode, use ``rickshaw -v``. 
  This will pretty print every generated input file.

- To run Rickshaw in generate-and-run mode, you can use either: 

  - ``rickshaw -rh`` (for HDF5 output) 
  - ``rickshaw -rs`` (for SQLite output)
  - **or both**

  All generated input files will immediately be run by Cyclus to the output file format(s) specified.

Cool note!
----------
The above options can be mixed to achieve your desired behavior, a la:

``rickshaw -n 10 -i test.py -v -rh -rs``







