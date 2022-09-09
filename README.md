# subcellular-api

This repo hosts a Python API for the subcellular application.
It allows users of the subcellular to download their existing models, run simulations in the cloud.

# Installation
To install the api, first clone the repo:
`git clone git@bbpgitlab.epfl.ch:nse/subcellular-api.git`

Then install the required dependences:
`pip install -r requirements.txt`

# Authentication

In order to be able to create and fetch models you will need you user id. To get it go to the subcellular app http://subcellular-bsp-epfl.apps.hbp.eu/ and on the top left corner click on `User` from the pop up copy the user id.

# Downloading models

To download your existing models simply run, make sure to provide your user id from the webapp

`download_models('myUserId')`

# Creating models

To create a model from a bngl file run

`create_model(path='example.bngl', name='Example model, user_id: '')`

*This command returns the id of the new model.*

Where user_id is a valid user id.

# Adding a geometry and mesh

To add a geometry and mesh to an existing model you will need 4 files (.json, .ele, .node, .face). 

`create_geometry(path='example.json', user_id: 'valid uuid', model_id: 'integer')`

    path: The path to any of the 4 files mentioned above, all 4 files must have the same name (e.g. spine.json, spine.ele, spine.node, spine.face).
    user_id: A valid uuid
    model_id: A valid model id, it is returned by the create_model command.
`


# Running simulations

In order to run a simulation you will need the model id as returned by the create_model command, the instantiate a Simulation:

`simulation = Simulation(model_id, user_id)`

Then you can run a simulation with:

```
id = simulation.run(
    t_end=1,
    dt=0.1,
    solver='tetexact'
    stimuli_path: 'Path to tsv file'
    )
```

The optional `stimuli_path` argument accepts a string with the path to a tsv file defining the stimuli.

This will start the simulation in the servers.

If you're doing it in a script, before downloading the results wait until the simulation is finished, otherwise you might get incomplete results.

```
from time import time
time.sleep(10)
```

Finally you can download the simulation results with:

`simulation.get_sim_traces()`
