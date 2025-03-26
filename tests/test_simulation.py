import pytest 
import numpy as np
import pyflowy as pfy
from pyflowy import util
from pathlib import Path

FILEPATH = Path(__file__).parent

def test_simulation(hawaii_example):

    toml_filepath, asc_filepath = hawaii_example

    input_params = pfy.flowycpp.parse_config( toml_filepath )
    input_params.write_thickness_every_n_lobes = 5000
    pfy.flowycpp.validate_settings(input_params)

    output_folder = Path(f"{FILEPATH}/output_test")
    # Remove any previous files because otherwise you just get more extra files and the old ones persist
    if output_folder.exists():
        [f.unlink() for f in output_folder.glob("*")]
        output_folder.rmdir()

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
