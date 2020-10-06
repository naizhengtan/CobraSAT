from ser_encodings import ENCODING_CLASSES
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
        if not value:
            encoding = key[0]
            polygraph = key[1]

            result, encoding, timings = run_encoding(encoding, polygraph)
            progress_object[key] = (result, timings)

            with open(PROGRESS_FILE, 'w') as progress_file:
                pickle.dump(progress_object, progress_file)

if __name__ == "__main__":
    read_percentages = [50, 75, 90]
    polygraph_size = range(100, 401, 50)
    polygraph_dir = 'polygraphs/workloads3'
    polygraphs = [f'{polygraph_dir}/chengR{read_percent}-{size}.polyg' 
                    for size, read_percent in product(polygraph_size, read_percentages)]
    experiments_params = product(ENCODING_CLASSES, polygraphs)
    progress_object = None

    if os.path.isfile(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'rb') as progress_file:
            progress_object = pickle.load(progress_file)
    else:
        progress_object = OrderedDict.fromkeys(experiments_params)

    run_experiment(progress_object)