from z3 import *
from encoding import Encoding
from mixins import MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress
from variables import generate_z3_vars, generate_z3_aux_vars, make_var_of_edge

class TransitiveTC1(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2, MixinPrintProgress):
    name = 'tc1'
    description = 'tc1 encoding from Janota17 in Z3. Transitive closure encoded directly with predicate logic in Z3.'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency = generate_z3_vars(total_nodes)
        self.aux = generate_z3_aux_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        # aux_of([i, j]) represents relation i R j
        var_of = make_var_of_edge(self.adjacency)
        aux_of = make_var_of_edge(self.aux)
        n = self.total_nodes

        self.encode_polygraph(var_of, edges, constraints)
        s = self.solver

        for begin in range(n):
            # s.add(Not(var_of([begin, begin]))) # No self-loops. Not part of the true encoding.
            s.add(Not(aux_of([begin, begin])))              # 1) irreflexivity
            for end in range(n):
                s.add(Implies(var_of([begin, end]),         # 3) closure of edges
                              aux_of([begin, end])))
                for mid in range(n):
                    connecting = And(aux_of([begin, mid]),  # 2) transitivity
                                     aux_of([mid, end]))
                    s.add(Implies(connecting, aux_of([begin, end])))
            self.print_progress(begin, n)
        print()

    def solve(self):
        return super().solve()

# # consider also: z3 with sat + tseitin tactics
# class TC1Dimacs(Encoding):
#     name = 'tc1-dimacs'
#     description = 'tc1 encoding in dimacs'

#     def __init__(self, total_nodes):
#         pass

#     def encode(self, edges, constraints):
#         # should write to some dimacs folder to solve from
#         pass
    
#     def solve(self):
#         # implement in child classes with different solvers?
#         pass