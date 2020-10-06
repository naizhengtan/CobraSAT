from monosat import *
from encoding import Encoding
from encoding.mixins import MixinPrintProgress

class Mono(Encoding, MixinPrintProgress):
    name = 'mono'
    description = 'Acyclicity of polygraph encoded with MonoSAT graph primitives.'

    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.graph = Graph()

    def encode(self, edges, constraints):
        for node_pair in edges:
            edge = self.graph.addEdge(*node_pair)
            Assert(edge)

        for constraint in constraints:
            e1 = self.graph.addEdge(*(constraint[0]))
            e2 = self.graph.addEdge(*(constraint[1]))
            Assert(And(Or(e1, e2), Or(Not(e1), Not(e2)))) # XOR

        Assert(self.graph.acyclic())

    def solve(self):
        return Solve()
