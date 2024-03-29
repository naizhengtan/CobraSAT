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
    generate_z3_int_aux_vars,
    make_var_of_edge
)

class TopoBitVec(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'topo-bv'
    description = 'Acyclicity encoded as embedded topological ordering. Using Z3 BitVec theory (unsigned integers) for ordering of nodes.'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.ordering = generate_z3_bitvec_aux_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        var_of = make_var_of_edge(self.adjacency)
        ordering_of = lambda node: self.ordering[node]

        n = self.total_nodes
        s = self.solver

        self.encode_polygraph(var_of, edges, constraints)

        for begin in range(n):
            for end in range(n):
                # edge from begin to end => ordering(begin) < ordering(end)
                less_than = ULT(ordering_of(begin), ordering_of(end))
                s.add(Implies(var_of([begin, end]), less_than))
            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()

    def variable_count(self, n, edges, constraints):
        return n**2 + n*int(math.ceil(math.log2(n)))

class TopoInt(TopoBitVec):
    name = 'topo-int'
    description = 'Similar to topo-bv, encoding acyclicity as embedded topological ordering, but with Z3 Integer theory for ordering of nodes.'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.ordering = generate_z3_int_aux_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        var_of = make_var_of_edge(self.adjacency)
        ordering_of = lambda node: self.ordering[node]

        n = self.total_nodes
        s = self.solver

        self.encode_polygraph(var_of, edges, constraints)

        for begin in range(n):
            for end in range(n):
                less_than = ordering_of(begin) < ordering_of(end)
                s.add(Implies(var_of([begin, end]), less_than))
            self.print_progress(begin, n)
        print()
