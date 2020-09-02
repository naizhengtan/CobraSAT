from encoding import Encoding
from formula.dimacs import to_dimacs
from formula.formula import *
from mixins import (
    MixinPrintProgress
)
from variables import (
    make_var_of_edge
)
import math

class BinaryLabeling(Encoding, MixinEncodePolygraphCNF, MixinPrintProgress):
    name = 'binary-labeling'
    description = ''

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = [[Atom(f'a:{origin},{dest}') for dest in range(total_nodes)] for origin in range(total_nodes)]
        bits = math.ceil(math.log(total_nodes, 2))
        self.ordering = [[Atom(f'o:{node},{bit}') for bit in range(int(bits))] for node in range(total_nodes)]

    def encode(self, edges, constraints):
        # writes it to temp file
        var_of = make_var_of_edge(self.adjacency)
        ordering_of = lambda node: self.ordering[node]

        n = self.total_nodes
        s = self.solver

        cnf = self.encode_polygraph(var_of, edges, constraints)

        for begin in range(n):
            for end in range(n): 
                # could precompute the formula and fill in the vars
                implies_ordering = Implies(var_of([begin, end]), lex(ordering_of(begin), ordering_of(end)))
                cnf.and_cnf(to_cnf(implies_ordering))
            self.print_progress(begin, n)
        print() 
        
        self.cnf = cnf
        to_dimacs(self.cnf)
        # talked with cheng: just use the command interface to run against temp dimacs file

    def solve(self):
        return 

def lex(a, b, index=0):
    if len(a) - index == 0:
        return FALSE 
    else:
        # a < b
        a_i, b_i = a[index], b[index]
        is_digit_less = And(Not(a_i), b_i)
        return Or(is_digit_less, And(Or(Not(a_i), b_i), lex(a, b, index + 1)