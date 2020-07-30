from abc import ABC, abstractmethod

class Formula(ABC):
    @abstractmethod
    def to_cnf(self):
        pass
    
    @abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return repr(self)

class UnaryOperator(Formula):
    def __init__(self, inner):
        self.inner = inner
    
    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.inner)})'

class BinaryOperator(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.left)} {repr(self.right)})'

class Atom(Formula):
    def __init__(self, name):
        self.name = name
    
    def to_cnf(self):
        return self
    
    def __repr__(self):
        return self.name

TRUE = Atom('TRUE')
FALSE = Atom('FALSE')

class Expandable(ABC):
    @abstractmethod
    def expand(self):
        pass

    def to_cnf(self):
        self.expand().to_cnf()

def unpack_ands(ands):
    if isinstance(ands.left, And):
        nested_ands = ands.left
        inner_clauses = ands.right
        return nested_ands, inner_clauses
    elif isinstance(ands.right, And):
        inner_clauses = ands.left
        nested_ands = ands.right
        return nested_ands, inner_clauses
    else: 
        return ands.left, ands.right

def clauses(cnf):
    if isinstance(cnf, And):
        nested_ands, inner_clauses = unpack_ands(cnf)
        yield inner_clauses
        for clause in clauses(nested_ands):
            yield clause
    else:
        yield cnf

class And(BinaryOperator):
    def to_cnf(self):
        return And(self.left.to_cnf(), self.right.to_cnf())

class Or(BinaryOperator):
    def to_cnf(self):
        left_cnf = self.left.to_cnf()
        right_cnf = self.right.to_cnf()

        acc = None
        for clause_from_left_cnf in clauses(left_cnf):
            for clause_from_right_cnf in clauses(right_cnf):
                if acc is None:
                    acc = Or(clause_from_left_cnf, clause_from_right_cnf)
                else:
                    acc = And(acc, Or(clause_from_left_cnf, clause_from_right_cnf))
        return acc 

class Not(UnaryOperator):
    def to_cnf(self):
        if isinstance(self.inner, Atom):
            return self
        if isinstance(self.inner, Not):
            return self.inner.to_cnf()
        elif isinstance(self.inner, And):
            left = self.inner.left
            right = self.inner.right
            return Or(Not(left), Not(right)).to_cnf()
        elif isinstance(self.inner, Or):
            left = self.inner.left
            right = self.inner.right
            return And(Not(left), Not(right)).to_cnf()
        elif isinstance(self.inner, Expandable):
            return Not(self.inner.expand()).to_cnf()
        else:
            raise Exception('unexpected inner!', self.inner)

class Implies(BinaryOperator, Expandable):
    def expand(self):
        return Or(Not(self.left), self.right)

class Iff(BinaryOperator, Expandable):
    def expand(self):
        left = self.left
        right = self.right
        return Or(And(left, right), And(Not(left), Not(right)))

class Paren(UnaryOperator, Expandable):
    def expand(self):
        return self.inner
    
    def __repr__(self):
        return f'({repr(self.inner)})'