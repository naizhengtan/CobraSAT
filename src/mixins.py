from z3 import *
from formula.cnf import *

# TODO: starting to think that helper functions might've been
# a better choice than mixins for some of these (e.g. print_progress)
class MixinEncodePolygraphZ3:
    def encode_polygraph(self, var_of, edges, constraints):
        s = self.solver

        for edge in edges:
            s.add(var_of(edge))

        for constraint in constraints:
            s.add(Xor(var_of(constraint[0]), var_of(constraint[1])))

class MixinWriteSMT2:
    filetype = 'smt2'

    def write_to_file(self, file_firstname):
        filename = file_firstname + self.filetype()
        with open(filename, 'w') as file:
            file.write(self.solver.to_smt2())

class MixinPrintProgress:
    def print_progress(self, iteration, n):
        print('\rprogress: {:.2f}%'.format(iteration* 100 / (n - 1)), end='')

class MixinEncodePolygraphCNF:
    def encode_polygraph(self, var_of, edges, constraints):
        cnf = CNF()
        for edge in edges:
            variable = var_of(edge)
            cnf.add_clause(Clause([literal(variable)]))
        