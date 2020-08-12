from abc import ABC, abstractmethod

def increment_var(current_var):
    # ts-<number>
    return f'ts-{(int(current_var[3:]) + 1)}'

# TODO: consider registering instead of using inheritance?
# TODO: could probably convert to_cnf et al to visitor pattern
class Formula(ABC):
    @abstractmethod
    def to_cnf_formula(self):
        pass

    @abstractmethod
    def tseitin(self, next_var):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return repr(self)

class UnaryOperator(Formula, ABC):
    def __init__(self, inner):
        self.inner = inner

    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.inner)})'

    def tseitin(self, next_var):
        inner_expr, inner_var, out_var = self.inner.tseitin(next_var)

        subexpr = tseitin_subexpr(inner_var, out_var)
        cnf_formula = And(inner_expr, subexpr)

        return cnf_formula, out, increment_var(out_var)

    @abstractmethod
    def tseitin_subexpr(self, inner_var, out_var):
        pass

class BinaryOperator(Formula, ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        op = type(self).__name__
        return f'({op} {repr(self.left)} {repr(self.right)})'
    
    def children(self):
        return [self.left, self.right]

class BinaryTseitin:
    def tseitin(self, next_var):
        l_expr, l_var, next_var = self.left.tseitin(next_var)
        r_expr, r_var, out_var = self.right.tseitin(next_var)

        subexpr = tseitin_subexpr(l_var, r_var, out_var)
        cnf_formula = And(l_expr, And(r_expr, subexpr))

        return cnf_formula, out_var, increment_var(out_var)

    @abstractmethod
    def tseitin_subexpr(self, left_var, right_var, out_var):
        pass

class Atom(Formula):
    def __init__(self, name):
        self.name = name

    def to_cnf_formula(self):
        return self

    def tseitin(self, next_var):
        return self, self.name, next_var

    def __repr__(self):
        return self.name

TRUE = Atom('TRUE')
FALSE = Atom('FALSE')

class Expandable(ABC):
    @abstractmethod
    def expand(self):
        pass

    def to_cnf_formula(self):
        return self.expand().to_cnf_formula()

    def tseitin(self):
        return self.expand().tseitin()

def clauses(cnf_formula):
    if isinstance(cnf_formula, And):
        for clause in clauses(cnf_formula.left):
            yield clause
        for clause in clauses(cnf_formula.right):
            yield clause
    else:
        yield cnf_formula

class And(BinaryTseitin, BinaryOperator):
    def to_cnf_formula(self):
        return And(self.left.to_cnf_formula(), self.right.to_cnf_formula())

    def tseitin_subexpr(self, l_var, r_var, out_var):
        # even AND needs a subexpr, in order to allow for chaining!
        clause_1 = Or(Not(l_var), Or(Not(r_var), out_var))
        clause_2 = Or(l_var, Not(out_var))
        clause_3 = Or(r_var, Not(out_var))

        subexpr = And(clause_1, And(clause_2, clause_3))
        return subexpr

class Or(BinaryTseitin, BinaryOperator):
    def to_cnf_formula(self):
        left_cnf_formula = self.left.to_cnf_formula()
        right_cnf_formula = self.right.to_cnf_formula()

        acc = None
        # distribution of <CNF> OR <CNF>
        for clause_from_left_cnf_formula in clauses(left_cnf_formula):
            for clause_from_right_cnf_formula in clauses(right_cnf_formula):
                if acc is None:
                    acc = Or(clause_from_left_cnf_formula, clause_from_right_cnf_formula)
                else:
                    acc = And(acc, Or(clause_from_left_cnf_formula, clause_from_right_cnf_formula))
        return acc

    def tseitin_subexpr(self, l_var, r_var, out_var):
        clause_1 = Or(l_var, Or(r_var, Not(out_var)))
        clause_2 = Or(Not(l_var), out_var)
        clause_3 = Or(Not(r_var), out_var)

        subexpr = And(clause_1, And(clause_2, clause_3))
        return subexpr

class Not(UnaryOperator):
    def to_cnf_formula(self):
        if isinstance(self.inner, Atom):
            return self
        if isinstance(self.inner, Not):
            return self.inner.to_cnf_formula()
        elif isinstance(self.inner, And):
            left = self.inner.left
            right = self.inner.right
            # DeMorgan's law for AND
            return Or(Not(left), Not(right)).to_cnf_formula()
        elif isinstance(self.inner, Or):
            left = self.inner.left
            right = self.inner.right
            # DeMorgan's law for OR
            return And(Not(left), Not(right)).to_cnf_formula()
        elif isinstance(self.inner, Expandable):
            return Not(self.inner.expand()).to_cnf_formula()
        else:
            raise Exception('unexpected inner!', self.inner)

    def tseitin_subexpr(self, inner_var, out_var):
        clause_1 = Or(Not(inner_var), Not(out_var))
        clause_2 = Or(inner_var, out_var)
        subexpr = And(clause_1, clause_2)

        return subexpr

class Implies(Expandable, BinaryOperator):
    def expand(self):
        return Or(Not(self.left), self.right)

class Iff(Expandable, BinaryOperator):
    def expand(self):
        left = self.left
        right = self.right
        return Or(And(left, right), And(Not(left), Not(right)))

def to_cnf_formula(formula):
    return formula.to_cnf_formula()

def make_atoms(names):
    return (*[Atom(name) for name in names.split()],) # unpack into a tuple!

def is_cnf_formula(formula):
    # TODO: there is a bug in the old code. what about the case when x AND (y OR z)?
    # x is not an OR! but this is valid CNF
    # double check that this fix is correct
    if isinstance(formula, And):
        return is_cnf_formula_BinaryOp(formula, (And, Or, Not, Atom))
        # return is_cnf_formula_BinaryOp(formula, (And, Or))
    elif isinstance(formula, Or):
        return is_cnf_formula_BinaryOp(formula, (Or, Not, Atom))
    elif isinstance(formula, Not):
        if isinstance(formula.inner, (Not, Atom)):
            return is_cnf_formula(formula.inner)
        else:
            return False
    elif isinstance(formula, Atom):
        return True

def is_cnf_formula_BinaryOp(formula, valid_child_instances):
    is_left_cnf = False
    if isinstance(formula.left, valid_child_instances):
        is_left_cnf = is_cnf_formula(formula.left)
    
    is_right_cnf = False
    if isinstance(formula.right, valid_child_instances):
        is_right_cnf = is_cnf_formula(formula.right)
        
    return is_left_cnf and is_right_cnf
