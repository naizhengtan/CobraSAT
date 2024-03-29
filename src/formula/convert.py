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
            pos_expr = inner.inner
            return pos_expr.accept(self)
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
    def __init__(self, prefix='ts-'):
        self.prefix = prefix
        self.var_count = 0

    def _next_var(self):
        self.var_count += 1
        # thank you garrett:
        # print(self.var_count)
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
        # technically Atom shouldn't be visited unless there is a single Atom in the CNF
        return CNF(), atom.name

    def visit_Not(self, not_formula):
        # in_var is the output variable of the inner, the input variable of the Not
        inner_cnf, in_var = not_formula.inner.accept(self)
        out_var = self._next_var()

        sub_cnf = Not_subexpr(in_var, out_var)

        # chain subexprs
        return inner_cnf.and_cnf(sub_cnf), out_var

    def visit_Or(self, or_formula):
        return self._transform_binary_op(or_formula, Or_subexpr)

    def visit_And(self, and_formula):
        return self._transform_binary_op(and_formula, And_subexpr)

def Not_subexpr(in_var, out_var):
    # (in OR out) AND (~in OR ~out)
    clause_1 = Clause([literal(in_var), literal(out_var)])
    clause_2 = Clause([literal(in_var, False), literal(out_var, False)])

    return CNF([clause_1, clause_2])

def And_subexpr(left_var, right_var, out_var):
    # subexpr: (a OR ~c) AND (b OR ~c) AND (c OR ~a OR ~b)
    clause_1 = Clause([literal(left_var), literal(out_var, False)])
    clause_2 = Clause([literal(right_var), literal(out_var, False)])
    clause_3 = Clause([literal(left_var, False), literal(right_var, False), literal(out_var)])

    return CNF([clause_1, clause_2, clause_3])

def Or_subexpr(left_var, right_var, out_var):
    clause_1 = Clause([literal(left_var), literal(right_var), literal(out_var, False)])
    clause_2 = Clause([literal(left_var, False), literal(out_var)])
    clause_3 = Clause([literal(right_var, False), literal(out_var)])

    return CNF([clause_1, clause_2, clause_3])

class ToIterativeTseitinCNF:
    def __init__(self, prefix='ts-'):
        self.prefix = prefix
        self.var_count = 0
        self.mapping = {}

    def _next_var(self):
        self.var_count += 1
        return self.prefix + str(self.var_count)

    def transform(self, formula):
        cnf = CNF()

        for node in formula.postorder():
            if isinstance(node, Atom):
                self.mapping[node] = node.name
            elif isinstance(node, Not):
                self.mapping[node] = self._next_var()
                out_var = self.mapping[node]
                in_var = self.mapping[node.inner]
                node_cnf = cnf.and_cnf(Not_subexpr(in_var, out_var))
            elif isinstance(node, Or):
                node_cnf = self._transform_binary_op_iterative(node, Or_subexpr, cnf)
            elif isinstance(node, And):
                node_cnf = self._transform_binary_op_iterative(node, And_subexpr, cnf)

        last_var = self.mapping[formula]
        return cnf.and_cnf(CNF([Clause([literal(last_var)])]))

    def _transform_binary_op_iterative(self, node, subexpr, cnf):
        left_var = self.mapping[node.left]
        right_var = self.mapping[node.right]

        self.mapping[node] = self._next_var()
        out_var = self.mapping[node]

        sub_cnf = subexpr(left_var, right_var, out_var)
        return cnf.and_cnf(sub_cnf)

def to_cnf(formula):
    return formula.accept(ToCNF())

def to_tseitin_cnf(formula):
    cnf, last_var = formula.accept(ToTseitinCNF())
    return cnf.and_cnf(CNF([Clause([literal(last_var)])]))

def to_tseitin_cnf_iterative(formula):
    return ToIterativeTseitinCNF().transform(formula)