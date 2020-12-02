from z3 import *
from encoding import Encoding
from encoding.mixins import MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress
from encoding.variables import generate_z3_vars, generate_z3_aux_vars, make_var_of_edge

class TC3(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'tc3'
    description = 'TC3 encoding from Janota17 in Z3. Similar to TC1 but without auxilary variables, due to monotonicity of polygraph acyclicity.'

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

    def variable_count(self, n, edges, constraints):
        return n**2
