from serializability import ENCODING_CLASSES
import serializability
from verify import run_encoding
from collections import OrderedDict
from itertools import product
import csv
import pickle
import os

TIMEOUT = 120000 # 20 min in ms
PROGRESS_FILE = 'results.pckl'

def run_experiment(progress_object):
    for key, value in progress_object.items():
        polygraph = key[0]
        encoding = key[1]
        # disable labeling encodings for now due to recursion limits
        # TODO: convert label encodings to use postorder generator traversal?
        if not value and not issubclass(encoding, (serializability.BinaryLabel, serializability.UnaryLabel)):
            result, encoding, timings = run_encoding(encoding, polygraph)
            progress_object[key] = (result, timings)

            with open(PROGRESS_FILE, 'wb') as progress_file:
                pickle.dump(progress_object, progress_file)

if __name__ == "__main__":
    read_percentages = [50, 75, 90]
    # polygraph_size = range(100, 401, 50)
    polygraph_size = range(100, 201, 50)
    polygraph_dir = 'polygraphs/workloads3'
    polygraphs = [f'{polygraph_dir}/chengR{read_percent}-{size}.polyg'
                    for size, read_percent in product(polygraph_size, read_percentages)]
    experiments_params = product(polygraphs, ENCODING_CLASSES)
    progress_object = None

    if os.path.isfile(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'rb') as progress_file:
            progress_object = pickle.load(progress_file)
    else:
        progress_object = OrderedDict.fromkeys(experiments_params)

    run_experiment(progress_object)
