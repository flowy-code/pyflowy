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