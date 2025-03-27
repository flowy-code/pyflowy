# pyflowy
Python bindings for Flowy

## Installation from Source

```bash
micromamba create -f environment.yml # For the first time only
micromamba activate pyflowyenv
meson setup build # To download flowy and C++ dependencies using meson wrap files
pip install .
```

If you have issues with `xtensor-python`, install it in the environment using:
```bash
micromamba install xtensor-python
```

Please note, that you will need to delete directories downloaded by `meson` if you want to pull the latest commits of the dependencies. Please do not delete the wrap file for `flowy`. Here's what you should do:
```bash
micromamba activate pyflowyenv
rm -rf subprojects 
git restore subprojects
meson setup build --wipe
pip install -e . --no-build-isolation
```

## How to Run a Simulation 

First, we will briefly describe the building blocks of the simulation, before describing how to run `PyFlowy` from `Python`.
Every simulation consists of flows, which are, in turn made up of lobes. Every lobe changes the topography, and therefore, subsequent flows are affected by previously deposited flows and lobes.

This beggars the question: why not just have one flow with many lobes? What's the difference between 1 flow with 50 lobes and 10 flows with 5 lobes each?

- 1 flow with 50 lobes: There is only one lobe with the largest thickness (the thickness of each lobe varies within each flow). 
- 10 flows with 5 lobes: Since there are 10 chains of lobes, there are 10 lobes with the largest thickness

Furthermore (perhaps more crucially; we do not know), parent lobes are only selected within the same flow. Practically, this means that the simulation consisting of a single large flow, will, on average, spread out further from the vent. 

This is enough to start with, to understand how to run `Flowy` and `PyFlowy`. The test `./tests/test_simulation.py` has a working example. 

```python
# A TOML file is parsed which creates an object with several input settings
# An example of the TOML file can be found at this link: 
# https://raw.githubusercontent.com/flowy-code/flowy/main/examples/KILAUEA2014-2015/input.toml
input_params = pfy.flowycpp.parse_config( toml_filepath )
# you can access and write to these settings 
input_params.write_thickness_every_n_lobes = 5000 # Writes out the thickness every time 5000 lobes have been processsed. Note: the initial DEM is ignored when writing out intermediate thicknesses. You can still place the intermediate thicknesses on top of the initial DEM

# These user-defined input settings should be validated (for instance, when the thickening_parameter is set to 1.0 then Flowy will crash. See Issue # 17 for details)
pfy.flowycpp.validate_settings(input_params)
input_params.output_folder = output_folder
# Asc and NetCDF file formats are supported by Flowy
input_params.source = asc_filepath # this example uses an .asc file as input. The topography is constructed from the initial DEM (which is the source here)

# Outputs can be created in the .asc file format, or the NetCDF file format (generally better), if you have compiled with NetCDF. The NetCDF file format can be compressed, and the user can control the data format in which the output will be saved (only in the case of NetCDF files). Also, some HDF5 viewers can be used to look at NetCDF files! 
input_params.output_settings.use_netcdf = True # this uses the NetCDF file format

# The crop to content functionality lets you "crop" parts of the output which have no lava. This can save a lot of space because DEMs are usually very big and the lava doesn't cover all of it  
input_params.output_settings.crop_to_content = True 

# You can save the NetCDF files with data types Short, Float or Double 
input_params.output_settings.data_type = pfy.flowycpp.StorageDataType.Short

# The Simulation class. The first argument is the InputParams class. The second argument is an optional seed. Just set it to None if you don't want to specify it
simulation = pfy.flowycpp.Simulation(input_params, None)
# The run function actually runs the entire simulation (for all flows and lobes)
simulation.run()
```

The example above creates and runs a simulation. However, it is also possible to change some input settings in the middle of a simulation and then restart it. Instead of using the `run` function of the simulation class, you would use the `steps` function. The `steps` function takes the number of steps as an argument and returns an enum (`Ongoing` or `Finished`) to indicate whether the simulation was completed or not. Note that the number of steps means the total number of lobes deposited (over all flows). The maximum number of steps that you can perform, therefore, is the product of the number of flows and the number of lobes in each flow. Note that although there are variables for `min_n_lobes` and `max_n_lobes`, in practice, we have found that this is always set to the same value (keeping the number of lobes in each flow constant). 

The following code snippet illustrates this functionality (see also `./tests/test_simulation.py`): 

```python
# Setup for the simulation 
input_params = pfy.flowycpp.parse_config( toml_filepath )
input_params.output_folder = output_folder
input_params.source = asc_filepath
# Create the Simulation object (with a seed of 0)
simulation = pfy.flowycpp.Simulation(input_params, 0)
# Some simulation parameters 
simulation.input.n_flows = 10 # Number of flows 
simulation.input.min_n_lobes = 50 # in practice the number of lobes is kept constant by keeping min_n_lobes equal to max_n_lobes
simulation.input.max_n_lobes = 50
# Various options that control the spreading of the lava
simulation.input.max_slope_prob = 0.0 
simulation.input.lobe_exponent = 0.0
simulation.input.inertial_exponent = 0.0
simulation.input.thickening_parameter = 0.0

# This loop keeps running the simulation in chunks of 100 steps, modifying the max_slop_prob each time
# until the simulation is completed  
while simulation.steps(100) == pfy.flowycpp.RunStatus.Ongoing:
    simulation.input.max_slope_prob += 0.1
```

## Citation 
    
https://doi.org/10.48550/arXiv.2405.20144



