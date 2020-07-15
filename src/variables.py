from z3 import *

def label(edge):
    return ','.join([str(node) for node in edge])

def label_aux(edge):
    return 'a' + label(edge)

def generate_z3_vars(n):
    # bools[begin][end]
    bools = [[Bool(label([begin, end])) for end in range(n)] for begin in range(n)]
    bools_aux = [[Bool(label_aux([begin, end])) for end in range(n)] for begin in range(n)]

    return bools, bools_aux
