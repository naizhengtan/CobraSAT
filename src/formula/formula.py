from abc import ABC, abstractmethod

class Formula(ABC):
    @abstractmethod
    def to_cnf(self):
        pass

    @abstractmethod
    def tseitin(self):
        pass

    @abstractmethod
    def iterate(self):
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

    def iterate(self):
        yield self
        for formula in self.inner.iterate():
            yield formula

class BinaryOperator(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.left)} {repr(self.right)})'

    def iterate(self):
        yield self

        for formula in self.left.iterate():
            yield formula

        for formula in self.right.iterate():
            yield formula

class Atom(Formula):
    def __init__(self, name):
        self.name = name

    def to_cnf(self):
        return self

    def tseitin(self):
        return self

    def __repr__(self):
        return self.name

    def iterate(self):
        yield self

TRUE = Atom('TRUE')
FALSE = Atom('FALSE')

class Expandable(ABC):
    @abstractmethod
    def expand(self):
        pass

    def to_cnf(self):
        self.expand().to_cnf()

def clauses(cnf):
    if isinstance(cnf, And):
        for clause in clauses(cnf.left):
            yield clause
        for clause in clauses(cnf.right):
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
        # distribution of <CNF> OR <CNF>
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
            # DeMorgan's law for AND
            return Or(Not(left), Not(right)).to_cnf()
        elif isinstance(self.inner, Or):
            left = self.inner.left
            right = self.inner.right
            # DeMorgan's law for OR
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

def to_cnf(formula):
    return formula.to_cnf()

def to_tseitin_cnf(formula):



