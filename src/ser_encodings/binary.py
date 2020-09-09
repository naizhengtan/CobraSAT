from encoding import Encoding
from formula.convert import to_cnf
from formula.dimacs import to_dimacs
from formula.formula import *
from mixins import (
    MixinEncodePolygraphCNF,
    MixinPrintProgress
)
from variables import (
    make_var_of_edge
)
from config import PROJECT_ROOT
import math
import os

class BinaryLabel(Encoding, MixinEncodePolygraphCNF, MixinPrintProgress):
    name = 'binary-label'
    description = ''
    folder = PROJECT_ROOT + '/dimacs/'
    filename = folder + name + '.dimacs'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = [[Atom(f'a:{origin},{dest}') for dest in range(total_nodes)] for origin in range(total_nodes)]
        bits = math.ceil(math.log(total_nodes, 2))
        self.ordering = [[Atom(f'o:{node},{bit}') for bit in range(int(bits))] for node in range(total_nodes)]

    def encode(self, edges, constraints):
        self._encode_and_write(edges, constraints, self.filename)

    def solve(self):
        return self._solve_from_dimacs(self.filename)

    def _encode_and_write(self, edges, constraints, filename):
        # writes it to temp file
        var_of = make_var_of_edge(self.adjacency)
        ordering_of = lambda node: self.ordering[node]
        n = self.total_nodes

        self.cnf = self.encode_polygraph(var_of, edges, constraints)

        for begin in range(n):
            for end in range(n): 
                # could precompute the formula and fill in the vars
                implies_ordering = Implies(var_of([begin, end]), lex(ordering_of(begin), ordering_of(end)))
                self.cnf.and_cnf(to_cnf(implies_ordering))
            self.print_progress(begin, n)
        print() 

        print('writing to file: ' + self.filename)
        dimacs = to_dimacs(self.cnf)
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        
        with open(self.filename, 'w') as f:
            f.write(dimacs)
        print('done writing encoding.')

    # should somehow support solver as a param
    def _solve_from_dimacs(self, filename):
        # talked with cheng: just use the command interface to run against temp dimacs file
        return 

def lex(a, b, index=0):
    if len(a) - index == 0:
        return FALSE 
    else:
        # a < b
        a_i, b_i = a[index], b[index]
        is_digit_less = And(Not(a_i), b_i)
        return Or(is_digit_less, And(Or(Not(a_i), b_i), lex(a, b, index + 1)))