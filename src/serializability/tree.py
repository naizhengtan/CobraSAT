from z3 import *
from encoding import Encoding
from encoding.mixins import (
    MixinEncodePolygraphZ3,
    MixinWriteSMT2,
    MixinPrintProgress
)
from encoding.variables import (
    generate_z3_vars,
    generate_z3_bitvec_aux_vars,
    make_var_of_edge
)

class TreeBV(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'tree-bv'
    description = 'Acyclicity encoded as tree reduction. Using Z3 BitVec theory (unsigned integers).'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.dists_to_leaf = generate_z3_bitvec_aux_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        var_of = make_var_of_edge(self.adjacency)
        dist_of = lambda node: self.dists_to_leaf[node]

        n = self.total_nodes
        s = self.solver

        self.encode_polygraph(var_of, edges, constraints)

        for begin in range(n):
            is_leaf = True
            at_least_one = False

            s.add(Not(var_of([begin, begin])))
            # s.add(UGE(dist_of(begin), 0))
            # s.add(ULE(dist_of(begin), n - 1))

            for end in range(n):
                if begin != end:
                    # If there is an edge from begin to end, begin is not a leaf
                    is_leaf = And(Not(var_of([begin, end])), is_leaf)

                    # children of <begin> are closer to leaf nodes
                    s.add(var_of([begin, end]) == UGT(dist_of(begin), dist_of(end)))

                    # at least one child has distance dist_of(begin) - 1
                    equals = dist_of(end) == (dist_of(begin) - 1)
                    at_least_one = Or(at_least_one, And(var_of([begin, end]), equals))

            s.add(is_leaf == (dist_of(begin) == 0))
            s.add(Or(is_leaf, at_least_one))

            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()

    def variable_count(self, n, edges, constraints):
        return n**2 + n*int(math.ceil(math.log2(n)))
