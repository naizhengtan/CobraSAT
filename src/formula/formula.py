from abc import ABC, abstractmethod
from collections import deque

# TODO: consider registering instead of using inheritance?
class Formula(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return repr(self)

    def accept(self, visitor):
        class_name = type(self).__name__
        return getattr(visitor, 'visit_' + class_name)(self)

    # postorder traversal, and also expand any Expandables
    def postorder(self):
        self = self.expand() if isinstance(self, Expandable) else self
        stack = deque([self])
        output = deque()

        while stack:
            current = stack.pop()
            if isinstance(current, UnaryOperator):
                current.inner = current.inner.expand() if isinstance(current.inner, Expandable) else current.inner
            elif isinstance(current, BinaryOperator):
                current.left = current.left.expand() if isinstance(current.left, Expandable) else current.left
                current.right = current.right.expand() if isinstance(current.right, Expandable) else current.right
            stack.extend(current.children())
            output.appendleft(current)

        return output

    def children(self):
        return []

class UnaryOperator(Formula, ABC):
    def __init__(self, inner):
        self.inner = inner

    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.inner)})'

    def children(self):
        return [self.inner]

class BinaryOperator(Formula, ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.left)} {repr(self.right)})'

    def children(self):
        return [self.left, self.right]

class Atom(Formula):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

TRUE = Atom('TRUE')
FALSE = Atom('FALSE')

class Expandable(ABC):
    @abstractmethod
    def expand(self):
        pass
    def accept(self, visitor):
        return self.expand().accept(visitor)

def clauses(cnf_formula):
    if isinstance(cnf_formula, And):
        for clause in clauses(cnf_formula.left):
            yield clause
        for clause in clauses(cnf_formula.right):
            yield clause
    else:
        yield cnf_formula

class And(BinaryOperator):
    pass

class Or(BinaryOperator):
    pass

class Not(UnaryOperator):
    pass

class Implies(Expandable, BinaryOperator):
    def expand(self):
        return Or(Not(self.left), self.right)

class Iff(Expandable, BinaryOperator):
    def expand(self):
        left = self.left
        right = self.right
        # return And(Implies(left, right).expand(), Implies(right, left).expand())
        return Or(And(left, right), And(Not(left), Not(right)))

def make_atoms(names):
    return (*[Atom(name) for name in names.split()],) # unpack into a tuple!