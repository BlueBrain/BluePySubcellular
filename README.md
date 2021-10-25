# subcellular-api

This repo hosts a Python API for the subcellular application.
It allows users of the subcellular to download their existing models, run simulations in the cloud.

# Authentication

In order to be able to download models you will need you user id. To get it go to the subcellular app http://subcellular-bsp-epfl.apps.hbp.eu/ and on the top left corner click on `User` from the pop up copy the user id.

# Downloading models

To download your existing models simply run, make sure to provide your user id from the webapp

`download_models('myUserId')`

# Running simulations

In order to run a simulation firt you need to load a model from it's BNGL source ,do so by instantiating a `Simulation`, pass the path where the `bngl` is located.

`simulation = Simulation('bngl_path')`

To schedule a simulation run, with the appropriate configuration, this will return the **simulation id**:

```
id = simulation.run(
    t_end=1,
    dt=0.1,
    solver='ode')
```


This will start the simulation in the servers.

If you're doing it in a script, before downloading the results wait until the simulation is finished, otherwise you might get incomplete results.

```
from time import time
time.sleep(10)
```

And then download the simulation results, pass the simulation id that was given by the simulation.run command:

`get_sim_traces('simulation_id')`
