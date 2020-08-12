from formula import *
from cnf import literal

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
