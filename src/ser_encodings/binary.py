from encoding import Encoding
from formula.convert import to_cnf, to_tseitin_cnf
from formula.dimacs import to_dimacs
from formula.cnf import simplify_cnf
from formula.formula import *
from mixins import (
    MixinEncodePolygraphCNF,
    MixinPrintProgress
)
from variables import (
    make_var_of_edge
)
from solvers import minisat_sat, z3_sat
from config import PROJECT_ROOT
import math
import os
from pathlib import Path

class BinaryLabel(Encoding, MixinEncodePolygraphCNF, MixinPrintProgress):
    name = 'binary-label'
    description = ''
    default_folder = PROJECT_ROOT + '/dimacs/'
    default_filename = default_folder + name + '.dimacs'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = [[Atom(f'a:{origin},{dest}') for dest in range(total_nodes)] for origin in range(total_nodes)]
        self.bits = math.ceil(math.log(total_nodes, 2))
        self.ordering = [[Atom(f'o:{node},{bit}') for bit in range(int(self.bits))] for node in range(total_nodes)]

    def encode(self, edges, constraints, **options):
        self.filename = options['outfile'] if 'outfile' in options else self.default_filename
        return self._encode_and_write(edges, constraints, self.filename)

    def solve(self):
        return self._solve_from_dimacs(self.filename)
    
    def _solve_from_dimacs(self, filename):
        raise NotImplementedError 

    def _encode_and_write(self, edges, constraints, filename):
        # writes it to temp file
        var_of = make_var_of_edge(self.adjacency)
        str_var_of = lambda edge: str(var_of(edge)) # encode_polygraph for dimacs expects strings
        ordering_of = lambda node: self.ordering[node]
        n = self.total_nodes

        self.cnf = self.encode_polygraph(str_var_of, edges, constraints)

        formula = TRUE 
        for begin in range(n):
            for end in range(n): 
                # could precompute the formula and fill in the vars
                implies_ordering = Implies(var_of([begin, end]), 
                                           lex(ordering_of(begin), ordering_of(end)))
                formula = And(implies_ordering, formula)
            self.print_progress(begin, n)
        print()

        ordering_cnf = simplify_cnf(to_tseitin_cnf(formula))
        self.cnf.and_cnf(ordering_cnf)
        
        dimacs = to_dimacs(simplify_cnf(self.cnf))

        print('writing to file: ' + filename)
        folder = Path(filename).stem
        if not os.path.isdir(folder):
            os.mkdir(folder)
        
        with open(filename, 'w') as f:
            f.write(dimacs)
        print('done writing encoding.')
        return filename

def lex(a, b, index=0):
    if index == len(a):
        return FALSE
    else:
        # a < b
        a_i, b_i = a[index], b[index]
        is_digit_less = And(Not(a_i), b_i)
        return Or(is_digit_less, And(Or(Not(a_i), b_i), lex(a, b, index + 1)))

class BinaryLabelMinisat(BinaryLabel):
    def _solve_from_dimacs(self, filename):
        return minisat_sat(filename)

class BinaryLabelZ3(BinaryLabel):
    def _solve_from_dimacs(self, filename):
        return z3_sat(filename)

class BinaryLabelYices(BinaryLabel):
    def _solve_from_dimacs(self, filename):
        return yices_sat(filename)