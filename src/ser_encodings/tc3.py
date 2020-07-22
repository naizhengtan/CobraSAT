from z3 import *
from encoding import Encoding
from mixins import MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress
from variables import generate_z3_vars, generate_z3_aux_vars, make_var_of_edge


def TC3(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'tc3'
    description = 'tc3 encoding from Janota17 in Z3, similar to tc1 but without auxilary variables'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        var_of = make_var_of_edge(self.adjacency)
        n = self.total_nodes

        self.encode_polygraph(var_of, edges, constraints)
        s = self.solver

        for begin in range(n):
            s.add(Not(var_of([begin, begin])))
            for end in range(n):
                for mid in range(n):
                    connecting = And(var_of([begin, mid]), var_of([mid, end]))
                    s.add(Implies(connecting, var_of([begin, end])))
            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()
