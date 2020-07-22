from os.path import realpath
from pathlib import Path

DATA_PATH = str(Path(realpath(__file__)).parents[1].joinpath('polygraphs'))


