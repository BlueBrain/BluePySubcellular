# BluePySubcellular

This repo hosts a Python API for the Subcellular application.
It allows users of the Subcellular application to download their existing models and to run simulations in the cloud.

# Installation

To install the API, first clone the repo:

`git clone https://github.com/BlueBrain/BluePySubcellular.git`

Then install the package using pip:

```
cd BluePySubcellular
pip install .
```


# Examples

The following section contain some examples showing how to use this API. For details on the Subcellular app please see the [documentation](https://subcellular-bsp-epfl.apps.hbp.eu/static/docs.html).

## Authentication

In order to be able to create and fetch models you need you `User id`. To get it go to the Subcellular app http://subcellular-bsp-epfl.apps.hbp.eu/ and click on `User` on the top right corner.


## Downloading models

To download your existing models simply run the following command:

    import BluePySubcellular
    BluePySubcellular.download_models("User id")

## Creating models

To create a model from a `bngl` file run

    model_id = BluePySubcellular.create_model(path="example.bngl", name="Example model", user_id="User id")

This command returns the `model_id` of the new model.

## Adding a geometry and mesh

To add a geometry and mesh to an existing model you will need 4 files describing the geometry (`.json`, `.ele`, `.node` and `.face` files).

    BluePySubcellular.create_geometry(path="example.json", user_id=user_id, model_id=model_id)

    path: The path to any of the 4 files mentioned above. All 4 files must have the same name (e.g. `spine.json, spine.ele, spine.node, spine.face`).
    user_id: A valid User id.
    model_id: A valid model id as returned e.g. from the `create_model` command.


## Running simulations

In order to run a simulation you will need the model id as returned by the create_model command, then instantiate a simulation:

    simulation = BluePySubcellular.Simulation(name, user_id, model_id, solver, dt, t_end, stimuli_path)
    
    name: Name of the simulation.
    user_id: A valid User id.
    model_id: A valid model id as returned e.g. from the `create_model` command.
    solver: Name of the solver (one of 'tetexact', 'tetopsplit', 'nfsim', 'ode' or 'ssa'; see the [documentation](https://subcellular-bsp-epfl.apps.hbp.eu/static/docs.html) for details).
    dt: Time step (in seconds, e.g `0.02`).
    t_end: Total simulation time (in seconds, e.g. `10.0`)
    stimuli_path: Optional string argument defining the path to a `.tsv` file containing the stimuli.


To run the simulation simply call:

    simulation.run()

which will start the simulation on the servers.

To monitor the progress of the simulation you can use:

    simulation.progress
    
to get the progress of the simulation (in %) and 

    simulation.status
    
to get the status of the simulation which can be 

    started: The simulation is running.
    error: An error occurred. Please consult the log on the Subcellular app.
    finished: The simulation has been finished.

To wait for the results you can use a loop:


    while simulation.status not in ["error", "finished"]:
        time.sleep(1)
        pass

Finally you can download the simulation results using

    traces = simulation.get_sim_traces()
    
to plot/analyze them further.      

# Citation
When you use this software, we kindly ask you to cite the following DOI (under "Cite as"):

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7225409.svg)](https://doi.org/10.5281/zenodo.7225409)


# Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology and from HBP SGA3.

Copyright (c) 2022 Blue Brain Project/EPFL
