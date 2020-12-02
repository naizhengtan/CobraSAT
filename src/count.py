from collections import OrderedDict
from itertools import product
from encoding.polygraph import load_polyg
import pickle
from serializability import *
import os

PROGRESS_FILE = 'count.pckl'

CLASSES = [TC1, TC3,
                    TopoBitVec,
                    Axiomatic,
                    BinaryLabelMinisat,
                    UnaryLabelMinisat]

if __name__ == "__main__":
    read_percentages = [50, 75, 90]
    polygraph_size = range(100, 401, 50)
    polygraph_dir = 'polygraphs/workloads3'
    polygraphs = [f'{polygraph_dir}/chengR{read_percent}-{size}.polyg'
                    for size, read_percent in product(polygraph_size, read_percentages)]
    experiments_params = product(polygraphs, CLASSES)
    results = {}

    prev_counts = {}

    if os.path.isfile(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'rb') as progress_file:
           prev_counts = pickle.load(progress_file)

    for params in experiments_params:
        polyg = params[0]
        encoding_class = params[1]

        class_name = encoding_class.name

        if class_name == 'binary-label-minisat':
            results[(class_name, polyg)] = prev_counts[(class_name, polyg)]
            continue

        print('Trying: ' + class_name + ', ' + polyg)

        n, edges, constraints = load_polyg(polyg)
        encoding = encoding_class(n)

        var_count = -1
        clause_count = -1
        try:
            var_count = encoding.variable_count(n, edges, constraints)
            print('> var: ' + str(var_count))
        except AttributeError:
            print('  Skipping var count...')

        try:
            clause_count = encoding.clause_count(n, edges, constraints)
            print('> clause: ' + str(clause_count))
        except AttributeError:
            print('  Skipping clause count...')

        results[(class_name, polyg)] = {
            'var': var_count,
            'clause': clause_count
        }

    with open(PROGRESS_FILE, 'wb') as progress_file:
        pickle.dump(results, progress_file)
