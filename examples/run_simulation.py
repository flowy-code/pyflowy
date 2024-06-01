import pyflowy as pfy
from pyflowy import util
from pathlib import Path

util.download_file_from_github( Path("./hawaii/input.toml"), relative_file_path="examples/KILAUEA2014-2015/input.toml" )
util.download_file_from_github( Path("./hawaii/test20m.asc"), relative_file_path="examples/KILAUEA2014-2015/test20m.asc" )

input_folder = Path("./hawaii")

input_params = pfy.flowycpp.parse_config( input_folder/"input.toml" )
input_params.output_folder = "./output_test"
input_params.source = input_folder / "test20m.asc"

simulation = pfy.flowycpp.Simulation(input_params, 1)
simulation.run()
