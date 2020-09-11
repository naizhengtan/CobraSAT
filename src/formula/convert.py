from formula.formula import *
from formula.cnf import *

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
# TODO: many of these transforms are wrong because the ToCNF transform is buggy
class ToTseitinCNF:
    def __init__(self, prefix='ts'):
        self.prefix = prefix
        self.var_count = 0

    def _next_var(self):
        self.var_count += 1
        return self.prefix + str(self.var_count)

    def _transform_binary_op(self, formula, subexpr):
        left_cnf, left_var = formula.left.accept(self)
        right_cnf, right_var = formula.right.accept(self)
        out_var = self._next_var()

        sub_cnf = subexpr(left_var, right_var, out_var)

        # join subexprs: (sub_CNF) AND (left_CNF) AND (right_CNF)
        return sub_cnf.and_cnf(left_cnf).and_cnf(right_cnf), out_var

    def visit_Atom(self, atom):
        # edge case might exist when Atom is only thing in CNF
        return CNF(), atom.name

    def visit_Not(self, not_formula):
        inner_cnf, in_var = not_formula.inner.accept(self)
        out_var = self._next_var()

        # (in OR out) AND (~in OR ~out)
        clause_1 = Clause([literal(in_var), literal(out_var)])
        clause_2 = Clause([literal(in_var, False), literal(out_var, False)])
        sub_cnf = CNF([clause_1, clause_2])

        # chain subexprs
        return inner_cnf.and_cnf(sub_cnf), out_var
    
    def visit_Or(self, or_formula):
        return self._transform_binary_op(or_formula, self._Or_subexpr)

    def _Or_subexpr(self, left_var, right_var, out_var):
        clause_1 = Clause([literal(left_var), literal(right_var), literal(out_var, False)])
        clause_2 = Clause([literal(left_var, False), literal(out_var)])
        clause_3 = Clause([literal(right_var, False), literal(out_var)])

        return CNF([clause_1, clause_2, clause_3])
        
    def visit_And(self, and_formula):
        return self._transform_binary_op(and_formula, self._And_subexpr)
    
    def _And_subexpr(self, left_var, right_var, out_var):
        # subexpr: (a OR ~c) AND (b OR ~c) AND (c OR ~a OR ~b)
        clause_1 = Clause([literal(left_var), literal(out_var, False)])
        clause_2 = Clause([literal(right_var), literal(out_var, False)])
        clause_3 = Clause([literal(left_var, False), literal(right_var, False), literal(out_var)])
        
        return CNF([clause_1, clause_2, clause_3])

def to_cnf(formula):
    return formula.accept(ToCNF())

def to_tseitin_cnf(formula):
    return formula.accept(ToTseitinCNF())[0]