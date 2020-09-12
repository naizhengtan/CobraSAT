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
        self.adjacency = [[f'a:{origin},{dest}' for dest in range(total_nodes)] for origin in range(total_nodes)]
        bits = total_nodes
        self.ordering = [[f'o:{node},{bit}' for bit in range(int(bits))] for node in range(total_nodes)]
        self.aux_U = [[[f'U:{i},{j},{k}' for k in range(total_nodes)] 
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

                lessunr_cnf = self._lessunr_circuit(i, j, n, self.adjacency, self.ordering, self.aux_U)
                cnf.and_cnf(lessunr_cnf)
    
                # 2. unary circuit
                if j >= 1:
                    cnf.add_clause(Clause([literal(self.ordering[i][j - 1], False), literal(self.ordering[i][j])]))
                
            self.print_progress(i, n)
        print() 

        self.cnf = cnf

        print('writing to file: ' + self.filename)
        dimacs = to_dimacs(self.cnf)
        with open(self.filename, 'w') as f:
            f.write(dimacs)
        print('done writing encoding.')

    def _lessunr_circuit(self, i, j, n, adjacency, ordering, aux_U):
        # 1. lessunr circuit: {clause_yi, clause_yj for all bits} AND clause_U
        cnf = CNF()

        clause_U = Clause()
        for bit in range(n):
            clause_yi = Clause([
                literal(adjacency[i][j], False),
                literal(ordering[i][bit], False),
                literal(aux_U[i][j][bit], False)
            ])
            clause_yj = Clause([
                literal(adjacency[i][j], False),
                literal(ordering[j][bit]),
                literal(aux_U[i][j][bit], False)
            ])
            
            cnf.add_clause(clause_yi)
            cnf.add_clause(clause_yj)
            clause_U.add_literal(literal(aux_U[i][j][bit]))

        cnf.add_clause(clause_U)
        return cnf

    def _solve_from_dimacs(self, filename):
        return minisat_dimacs(filename)