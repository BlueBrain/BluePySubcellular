# BluePySubcellular

This repo hosts a Python API for the subcellular application.
It allows users of the subcellular application to download their existing models and to run simulations in the cloud.

# Installation

To install the API, first clone the repo:

`git clone git@bbpgitlab.epfl.ch:nse/subcellular-api.git`

Then install the package using pip:

`pip install .`


# Examples

The following section contain some examples showing how to use this API.

## Authentication

In order to be able to create and fetch models you need you `User id`. To get it go to the subcellular app http://subcellular-bsp-epfl.apps.hbp.eu/ and click on `User` on the top right corner.


## Downloading models

To download your existing models simply run the following command

`download_models('User id')`


## Creating models

To create a model from a `bngl` file run

`create_model(path='example.bngl', name='Example model', user_id: 'User id')`

This command returns the id of the new model.

## Adding a geometry and mesh

To add a geometry and mesh to an existing model you will need 4 files (.json, .ele, .node, .face).

`create_geometry(path='example.json', user_id: 'User id', model_id: 'integer')`

    path: The path to any of the 4 files mentioned above, all 4 files must have the same name (e.g. spine.json, spine.ele, spine.node, spine.face).
    user_id: A valid User id 
    model_id: A valid model id, it is returned by the create_model command.


## Running simulations

In order to run a simulation you will need the model id as returned by the create_model command, then instantiate a simulation:

`simulation = Simulation(name, model_id, user_id, solver, dt, t_end, stimuli_path)`

Where solver is one of 'tetexact', 'tetopsplit', 'nfsim', 'ode' or 'ssa'.

The optional `stimuli_path` argument accepts a string with the path to a `tsv` file defining the stimuli.

To run the simulation simply call:

`simulation.run()`

This will start the simulation on the servers.

To monitor the progress of the simulation you can use:

`simulation.progress` and `simulation.status`

To wait for the results you can use a loop:

```
while simulation.status != 'completed':
    pass
```

Finally you can download the simulation results with:

`simulation.get_sim_traces()`

# Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology and from HBP SGA3.

Copyright (c) 2022 Blue Brain Project/EPFL
