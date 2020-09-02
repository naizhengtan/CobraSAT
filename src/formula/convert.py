from formula.formula import *
from formula.cnf import *

# And -> cnf
# Or -> clause
# Not | Atom -> literal
# should probably just have converted formula directly to cnf
# instead of having cnf_formula as an intermediate step
# TODO: how do i refactor this nicely (if i am keeping this step)
def cnf_formula_to_cnf(cnf_formula):
    # if not is_cnf_formula(formula):
    #     raise Exception('not a cnf formula!')
    if isinstance(cnf_formula, And):
        cnf = []
        for child in cnf_formula.children():
            if isinstance(child, And):
                cnf.extend(cnf_formula_to_cnf(child))
            elif isinstance(child, Or):
                cnf.append(cnf_formula_to_cnf(child))
            elif isinstance(child, (Not, Atom)):
                cnf.append([cnf_formula_to_cnf(child)]) # wrap in list
        return cnf
    elif isinstance(cnf_formula, Or):
        clause = []
        for child in cnf_formula.children():
            if isinstance(child, Or):
                clause.extend(cnf_formula_to_cnf(child))
            elif isinstance(child, (Not, Atom)):
                clause.append(cnf_formula_to_cnf(child))
        return clause
    elif isinstance(cnf_formula, Not):
        inner = cnf_formula
        assert isinstance(inner, Atom)
        return literal(inner.name, False)
    elif isinstance(cnf_formula, Atom):
        return literal(cnf_formula.name, True)

# Formula -> CNF
# CNF = nil | (clause, CNF)
class ToCNF:
    def visit_Atom(self, atom):
        return CNF([Clause([literal(atom.name)])])
    
    def visit_Not(self, not_formula):
        inner = not_formula.inner
        if isinstance(inner, Not):
            return inner.accept(self)
        elif isinstance(inner, Atom):
            return CNF([Clause([literal(inner.name, False)])])
        elif isinstance(inner, And):
            left, right = inner.children()
            return Or(Not(left), Not(right)).accept(self)
        elif isinstance(inner, Or):
            left, right = inner.children()
            return And(Not(left), Not(right)).accept(self)
        elif isinstance(inner, Expandable):
            return Not(inner.expand()).accept(self)
        else:
            raise Exception("not a valid inner formula type")
    
    def visit_Or(self, or_formula):
        left_cnf = or_formula.left.accept(self)
        right_cnf = or_formula.right.accept(self)

        cnf = CNF()
        for l_clause in left_cnf:
            for r_clause in right_cnf:
                distr_clause = or_clauses(l_clause, r_clause)
                cnf.add_clause(distr_clause)
        return cnf

    def visit_And(self, and_formula):
        left_cnf = and_formula.left.accept(self)
        right_cnf = and_formula.right.accept(self)
        return left_cnf.and_cnf(right_cnf)

# formula.accept(ToTseitinCNF) -> (CNF, varname: str)
class ToTseitinCNF:
    def __init__(self, prefix='ts'):
        self.prefix = prefix
        self.var_count = 0

    def _next_var(self):
        self.var_count += 1
        return self.prefix + str(self.var_count)

    def _binary_op_transform(self):
        pass

    def visit_Atom(self, atom):
        cnf = CNF([Clause([literal(atom.name)])])
        return (cnf, atom.name)
    
    def visit_Not(self, not_formula):
        inner_cnf, in_var = not_formula.inner.accept(self)
        out_var = self._next_var()

        # (~in OR out)
        sub_cnf = CNF([Clause([literal(in_var, False), literal(out_var)])])

        # chain subexprs
        return inner_cnf.and_cnf(sub_cnf)
    
    def visit_Or(self, or_formula):
        left_cnf, left_var = or_formula.left.accept(self)
        right_cnf, right_var = or_formula.right.accept(self)
        out_var = self._next_var()

        # subexpr: (~out_var AND ~left_var AND ~right_var) 
        clause_1 = Clause([literal(out_var, False)])
        clause_2 = Clause([literal(left_var, False)])
        clause_3 = Clause([literal(right_var, False)])
        sub_cnf = CNF([clause_1, clause_2, clause_3])
        
        # (sub_CNF) AND (left_CNF) AND (right_CNF)
        return sub_cnf.and_cnf(left_cnf).and_cnf(right_cnf)