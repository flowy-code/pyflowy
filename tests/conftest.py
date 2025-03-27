from pathlib import Path 
from pyflowy import util
import pytest

FILEPATH = Path(__file__).parent

@pytest.fixture
def hawaii_example() -> tuple[Path, Path]:
    toml_filepath = Path(f"{FILEPATH}/hawaii/input.toml")
    asc_filepath = Path(f"{FILEPATH}/hawaii/test20m.asc")
    util.download_file_from_github( toml_filepath, relative_file_path="examples/KILAUEA2014-2015/input.toml" )
    util.download_file_from_github( asc_filepath, relative_file_path="examples/KILAUEA2014-2015/test20m.asc" )
    return toml_filepath, asc_filepath

@pytest.fixture
def output_folder() -> Path:
    output_folder = Path(f"{FILEPATH}/output_test")
    # Remove any previous files because otherwise you just get more extra files and the old ones persist
    if output_folder.exists():
        [f.unlink() for f in output_folder.glob("*")]
        output_folder.rmdir()

    return output_folder