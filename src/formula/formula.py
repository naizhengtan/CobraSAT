from abc import ABC, abstractmethod

import cnf
from cnf import CNF

class Formula(ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def to_cnf(self):
        # technically order of operations will be preserved from inner
        # to outer, due to stack
        pass

class VarFormula(Formula):
    def __init__(self, name):
        self.name = name
    
    def to_cnf(self):
        return CNF.init_from_var(self.name)

class AndFormula(Formula):
    def to_cnf(self):
        return cnf.AND(self.left.to_cnf(), self.right.to_cnf())

class OrFormula(Formula):

        
