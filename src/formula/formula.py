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
        return name

TRUE = Atom('TRUE')
FALSE = Atom('FALSE')

def unpack_ands(ands):
    if isinstance(ands.left, And) and isinstance(ands.right, Or):
        nested_ands = ands.left
        inner_ors = ands.right
        return nested_ands, inner_ors
    elif isinstance(ands.left, Or) and isinstance(ands.right, And):
        inner_ors = ands.left
        nested_ands = ands.right
        return nested_ands, inner_ors
    else: 
        raise Exception('not in cnf')

def clauses(cnf):
    if isinstance(cnf, And):
        nested_ands, inner_ors = unpack_ands(cnf)
        yield inner_ors
        yield walk_cnf(nested_ands)
    else:
        yield cnf

class And(BinaryOperator):
    def to_cnf(self):
        return And(self.left.to_cnf(), self.right.to_cnf())

class Or(BinaryOperator):
    def to_cnf(self):
        # distribute ANDs
        left_cnf = self.left.to_cnf()
        right_cnf = self.right.to_cnf()
        
        ands = TRUE
        for clause_from_left_cnf in clauses(left_cnf):
            for clause_from_right_cnf in clauses(right_cnf):
                ands = And(ands, Or(clause_from_left_cnf, clause_from_right_cnf))
        return ands.to_cnf()

class Not(UnaryOperator):
    def to_cnf(self):
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
        else:
            return Not(self.inner.to_cnf())

class Implies(BinaryOperator):
    def to_cnf(self):
        return Or(Not(self.left), self.right).to_cnf()

class Iff(BinaryOperator):
    def to_cnf(self):
        left = self.left
        right = self.right
        return Or(And(left, right), And(Not(left), Not(right))).to_cnf()

class Paren(UnaryOperator):
    def to_cnf(self):
        return self.inner.to_cnf()
    
    def __repr__(self):
        return f'({repr(self.inner)})'