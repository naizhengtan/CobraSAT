from z3 import *
from encoding import Encoding
from encoding.mixins import MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress
from encoding.variables import generate_z3_vars, generate_z3_aux_vars, make_var_of_edge

class TC(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'tc'
    description = "Acyclicity encoded with transitive closure using Z3's transitive closure feature."

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        var_of = make_var_of_edge(self.adjacency)
        n = self.total_nodes

        self.encode_polygraph(var_of, edges, constraints)
        s = self.solver

        R = Function('R', IntSort(), IntSort(), BoolSort()) # relation
        TC_R = TransitiveClosure(R)

        for begin in range(n):
            s.add(Not(TC_R(begin, begin)))
            for end in range(n):
                if begin != end:
                    s.add(Implies(var_of([begin, end]), R(begin, end)))
            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()

    def variable_count(self):
        return n**2