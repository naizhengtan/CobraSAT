from z3 import *
from encoding import Encoding
from encoding.mixins import MixinWriteSMT2, MixinPrintProgress
from encoding.variables import generate_z3_vars, make_var_of_edge

class Axiomatic(Encoding, MixinWriteSMT2, MixinPrintProgress):
    name = 'axiom'
    description = 'Direct encoding of serializability (SER) using axiomatic framework from Biswas19.'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.ordering = generate_z3_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        # let var_of([i, j]) represent transaction i before j
        # var represents ordering relation
        var_of = make_var_of_edge(self.ordering)
        n = self.total_nodes

        s = self.solver

        for edge in edges:
            s.add(var_of(edge)) # known WR edges must be ordered

        for constraint in constraints:
            # Notice how constraints line up to axioms
            t1 = constraint[1][1]
            t2 = constraint[0][1]
            t3 = constraint[0][0]

            s.add(Implies(var_of([t2, t3]), var_of([t2, t1]))) # Axiom for Serializability

        # Strict total ordering: 1) transitive, 2. trichotomous (asymmetric and semi-connex)
        # asymmetric = irreflexive and antisymmetric
        for begin in range(n):
            s.add(Not(var_of([begin, begin]))) # irreflexive
            for end in range(n):
                if begin != end:
                    s.add(Xor(var_of([begin, end]), var_of([end, begin]))) # asymmetric and semi-connex
                for middle in range(n):
                    if begin != middle and end != middle:
                        begin_middle_end = And(var_of([begin, middle]), var_of([middle, end]))
                        s.add(Implies(begin_middle_end, var_of([begin, end]))) # transitive

            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()

    def variable_count(self, n, edges, constraints):
        # unique variables?
        # redundancy in pairings of begin, middle, end
        # [begin/middle/end, begin/middle/end] -> n^2
        return n**2

# class AxiomaticLinearOrder(Encoding, MixinWriteSMT2, MixinPrintProgress):
# TODO: may not possible with z3 currently, since Z3's linear order is >= instead of strict inequality
# probably possible to add addition assertions to fix this
