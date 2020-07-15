from z3 import *
from abc import ABC, abstractmethod
from variables import generate_z3_vars

class Encoding(ABC):
    @abstractmethod
    def __init__(self, total_nodes):
        pass

    @abstractmethod
    def encode(self, total_nodes, edges, constraints):
        pass

    @abstractmethod
    def solve(self):
        results = self.solver.check()
        if results == 'sat':
            return True
        elif results == 'unsat':
            return False

    @property
    def filetype(self):
        return None

    def write_to_file(self):
        raise Exception("This encoding does not support writing to file")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

def make_var_of_edge(variables):
    return lambda edge: variables[edge[0]][edge[1]]

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

class TC1(Encoding, MixinEncodePolygraphZ3, MixinWriteSMT2):
    name = 'tc1'
    description = 'tc1 encoding from Janota17'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.adjacency, self.aux = generate_z3_vars(total_nodes)
        self.solver = Solver()

    def encode(self, edges, constraints):
        # aux_of([i, j]) represents relation i R j
        var_of = make_var_of_edge(self.adjacency)
        aux_of = make_var_of_edge(self.aux)
        n = self.total_nodes

        self.encode_polygraph(var_of, edges, constraints)
        s = self.solver

        for begin in range(n):
            # s.add(Not(var([begin, begin]))) # No self-loops. Not part of the true encoding.
            s.add(Not(aux_of([begin, begin])))              # 1) irreflexivity
            for end in range(n):
                s.add(Implies(var_of([begin, end]),         # 3) closure of edges
                              aux_of([begin, end])))
                for mid in range(n):
                    connecting = And(aux_of([begin, mid]),  # 2) transitivity
                                     aux_of([mid, end]))

            print('\r{:.2f}%'.format(begin / n), end='')
        print('\n')

    def solve(self):
        return super(TC1, self).solve()

