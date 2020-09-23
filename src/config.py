from os.path import realpath
from pathlib import Path

PROJECT_ROOT = str(Path(realpath(__file__)).parents[1])
DEFAULT_DIMACS_FOLDER = PROJECT_ROOT + '/dimacs/'
DATA_PATH = str(Path(realpath(__file__)).parents[1].joinpath('polygraphs'))

