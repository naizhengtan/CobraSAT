from encoding import Encoding
from formula.cnf import *
from formula.dimacs import to_dimacs
from formula.formula import *
from mixins import (
    MixinPrintProgress,
    MixinEncodePolygraphCNF
)
from variables import (
    make_var_of_edge
)
from config import PROJECT_ROOT
from solvers import minisat_dimacs
import math

class UnaryLabel(Encoding, MixinEncodePolygraphCNF, MixinPrintProgress):
    name = 'unary-label'
    description = ''
    folder = PROJECT_ROOT + '/dimacs/'
    filename = folder + name + '.dimacs'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = [[Atom(f'a:{origin},{dest}') for dest in range(total_nodes)] for origin in range(total_nodes)]
        bits = total_nodes
        self.ordering = [[Atom(f'o:{node},{bit}') for bit in range(int(bits))] for node in range(total_nodes)]
        self.aux_U = [[[Atom(f'U:{i},{j},{k}') for k in range(total_nodes)] 
                        for j in range(total_nodes)] 
                            for i in range(total_nodes)] # U[i][j][k]

    def encode(self, edges, constraints):
        # self._encode_and_write(edges, constraints, 'filename' in if options['filename'])
        self._encode_and_write(edges, constraints, self.filename)

    def solve(self):
        return self._solve_from_dimacs(self.filename)

    def _encode_and_write(self, edges, constraints, filename):
        # writes it to temp file
        var_of = make_var_of_edge(self.adjacency)
        n = self.total_nodes
        cnf = self.encode_polygraph(var_of, edges, constraints)

        for i in range(n):
            for j in range(n): 
                clause_U = Clause()

                for bit in range(n):
                    clause_yi = Clause([
                        literal(self.adjacency[i][j], False),
                        literal(self.ordering[i][bit], False),
                        literal(self.aux_U[i][j][bit], False)
                    ])
                    clause_yj = Clause([
                        literal(self.adjacency[i][j], False),
                        literal(self.ordering[j][bit]),
                        literal(self.aux_U[i][j][bit], False)
                    ])

                    cnf.add_clause(clause_yi)
                    cnf.add_clause(clause_yj)
                    clause_U.add_literal(literal(self.aux_U[i][j][bit]))
                
                cnf.add_clause(clause_U)
            self.print_progress(i, n)
        print() 

        self.cnf = cnf

        print('writing to file: ' + self.filename)
        dimacs = to_dimacs(self.cnf)
        with open(self.filename, 'w') as f:
            f.write(dimacs)
        print('done writing encoding.')

    def _solve_from_dimacs(self, filename):
        return minisat_dimacs(filename)