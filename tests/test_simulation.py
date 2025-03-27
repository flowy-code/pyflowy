import pytest 
import numpy as np
import pyflowy as pfy
from pyflowy import util
from pathlib import Path

FILEPATH = Path(__file__).parent

def test_simulation(hawaii_example, output_folder):

    toml_filepath, asc_filepath = hawaii_example

    input_params = pfy.flowycpp.parse_config( toml_filepath )
    input_params.write_thickness_every_n_lobes = 5000
    pfy.flowycpp.validate_settings(input_params)

    input_params.output_folder = output_folder
    input_params.source = asc_filepath

    # Change some of the output settings
    input_params.output_settings.use_netcdf = True
    input_params.output_settings.crop_to_content = True
    input_params.output_settings.data_type = pfy.flowycpp.StorageDataType.Short

    simulation = pfy.flowycpp.Simulation(input_params, None)
    simulation.run()

    assert Path(output_folder/f"{input_params.run_name}_thickness_after_{input_params.write_thickness_every_n_lobes}_lobes.nc").exists()
    # There is only one "masking threshold" value but internally this is a list
    assert Path(output_folder/f"{input_params.run_name}_thickness_masked_{input_params.masking_threshold[-1]}.nc").exists()
    assert Path(output_folder/f"{input_params.run_name}_hazard_full.nc").exists()
    # Same deal for the masking threshold for the hazard
    assert Path(output_folder/f"{input_params.run_name}_hazard_masked_{input_params.masking_threshold[-1]}.nc").exists()
    # Make sure that this summary file was written 
    assert Path(output_folder / f"{input_params.run_name}_avg_thick.txt").exists()


def test_simulation_with_steps(hawaii_example, output_folder):
    toml_filepath, asc_filepath = hawaii_example

    input_params = pfy.flowycpp.parse_config( toml_filepath )
    input_params.write_thickness_every_n_lobes = 100
    pfy.flowycpp.validate_settings(input_params)

    input_params.output_folder = output_folder
    input_params.source = asc_filepath

    # Change some of the output settings
    input_params.output_settings.use_netcdf = True
    input_params.output_settings.crop_to_content = True
    input_params.output_settings.data_type = pfy.flowycpp.StorageDataType.Short

    simulation = pfy.flowycpp.Simulation(input_params, 0)

    simulation.input.n_flows = 10
    simulation.input.min_n_lobes = 50
    simulation.input.max_n_lobes = 50
    simulation.input.max_slope_prob = 0.0
    simulation.input.lobe_exponent = 0.0
    simulation.input.inertial_exponent = 0.0
    simulation.input.thickening_parameter = 0.0

    while simulation.steps(100) == pfy.flowycpp.RunStatus.Ongoing:
        simulation.input.max_slope_prob += 0.1

    assert Path(output_folder/f"{input_params.run_name}_thickness_after_{input_params.write_thickness_every_n_lobes}_lobes.nc").exists()