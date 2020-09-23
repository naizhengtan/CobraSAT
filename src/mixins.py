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

        for constraint in constraints:
            one_true = Clause([literal(var_of(constraint[0])), 
                              literal(var_of(constraint[1]))])
            one_false = Clause([literal(var_of(constraint[0]), False), 
                               literal(var_of(constraint[1]), False)])
            # XOR:
            cnf.add_clause(one_true)
            cnf.add_clause(one_false)

        return cnf

class MixinUseExistingEncode:
    def encode(self, edges, constraints, **options):
        # don't reencode if outfile exists
        if options.get('use_existing') and options['outfile'] == self.filename and os.path.isfile(self.filename):
            return self.filename
        else:
            self.filename = options['outfile'] if 'outfile' in options else self.default_filename
            return self._encode_and_write(edges, constraints, self.filename)