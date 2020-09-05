from encoding import Encoding
from formula.dimacs import to_dimacs
from formula.formula import *
from mixins import (
    MixinPrintProgress,
)
from variables import (
    make_var_of_edge
)
import math

class UnaryLabeling(Encoding, MixinEncodePolygraphCNF, MixinPrintProgress):
    name = 'unary-labeling'
    description = ''
    temp_file = ''

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = [[Atom(f'a:{origin},{dest}') for dest in range(total_nodes)] for origin in range(total_nodes)]
        bits = total_nodes
        self.ordering = [[Atom(f'o:{node},{bit}') for bit in range(int(bits))] for node in range(total_nodes)]
        self.aux_U = [[[ for k in range(total_nodes)] for j in range(total_nodes)] for i in range(total_nodes)] # U[i][j][k]

    def encode(self, edges, constraints):
        self._encode_and_write(edges, constraints, self.temp_file)

    def _encode_and_write(self, edges, constraints, file):
        # writes it to temp file
        n = self.total_nodes
        cnf = self.encode_polygraph(var_of, edges, constraints)

        for i in range(n):
            for j in range(n): 
                clause_U = Clause()

                for bit in range(n):
                    clause_yi = Clause([
                        literal(self.adjacency[i][j]), False),
                        literal(self.ordering[i][bit]), False),
                        literal(self.aux_U[i][j][bit], False)
                    ])
                    clause_yj = Clause([
                        literal(self.adjacency[i][j], False),
                        literal(self.ordering[j][bit]),
                        literal(self.aux_U[i][j][bit], False)
                    ])

                    cnf.add_clause(clause_yi)
                    cnf.add_clause(clause_y)
                    clause_U.add_literal(literal(self.aux_U[i][j][bit]))
                
                cnf.add_clause(clause_U)
            self.print_progress(begin, n)
        print() 
        
        to_dimacs(self.cnf)

    def solve(self):
        return self._solve_and_delete(self.temp_file)
    
    def _solve_and_delete(self):
        pass