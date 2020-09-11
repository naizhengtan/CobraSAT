# cnf is a list of clauses
# clause is a list of literals
# literal is (name: str, pos: bool)

# dimacs:
# top can have comment lines, start with c
# problem line: p cnf <vars> <clauses>
# clause line: <int> <int> ... 0
# where int is the var number, and -i as NOT(ith var)

def literal(name, is_positive=True):
    assert isinstance(name, str)
    return (name, is_positive)

def simplify_cnf(cnf):
    simplified = CNF()

    for clause in cnf:
        simplified_clause = simplify_clause(clause)
        if simplified_clause:
            simplified.add_clause(simplified_clause)
    
    return simplified

def simplify_clause(clause):
    # simple rules:
    # Normalize !TRUE and !FALSE to FALSE and TRUE
    # 1. if TRUE in clause then remove clause
    # 2. if clause has both Var and !Var, remove clause
    # 3. remove FALSE from clauses
    
    seen = {} # let seen[Var] = True means positive literal seen
    simplified = Clause()
    for literal in clause:
        literal = normalize_literal(literal)
        name, is_positive = literal

        if name != 'FALSE':
            if name == 'TRUE':
                return Clause([])
            elif name in seen:
                if is_positive != seen[name]: # both Var, !Var are in clause => clause is always true
                    return Clause([])
            else:
                simplified.add_literal(literal)
                seen[name] = is_positive
     
    return simplified

def normalize_literal(literal):
    name, is_positive = literal
    is_tf = name == 'TRUE' or name == 'FALSE'

    if is_tf and not is_positive:
        return ('TRUE' if name == 'FALSE' else 'FALSE', not is_positive)
    else:
        return literal

class CNF:
    def __init__(self, clauses=None):
        # cnf = CNF() # totally hangs when empty list is default param??
        # turns out that python will use the same list every time...
        # classic pass by reference as value
        if clauses is None:
            clauses = []
        assert not clauses or isinstance(clauses[0], Clause)
        self.clauses = clauses

    def and_cnf(self, cnf):
        assert isinstance(cnf, CNF)
        self.clauses.extend(cnf.clauses)
        return self
    
    def add_clause(self, clause):
        assert isinstance(clause, Clause)
        self.clauses.append(clause)
        return self
    
    def __iter__(self):
        return iter(self.clauses)
    
    def __repr__(self):
        return ' AND '.join([str(clause) for clause in self])

class Clause:
    def __init__(self, literals=None):
        if literals is None:
            literals = []

        assert not literals or isinstance(literals[0], tuple)
        self.literals = literals
    
    def or_clause(self, clause):
        assert isinstance(clause, Clause)
        self.literals.extend(clause.literals)
        return self
    
    def add_literal(self, literal):
        self.literals.append(literal)
        return self

    def __iter__(self):
        return iter(self.literals)
    
    def __repr__(self):
        return f'({" OR ".join([literal_to_str(literal) for literal in self])})'
    
    def __bool__(self):
        return bool(self.literals)

def and_cnfs(cnf_1, cnf_2):
    return CNF(cnf_1.clauses + cnf_2.clauses)

def or_clauses(clause_1, clause_2):
    return Clause(clause_1.literals + clause_2.literals)

def literal_to_str(literal):
    name, is_positive = literal
    sign = '' if is_positive else '~'
    return f'{sign}{name}'

# def is_equisatifiable(formula_1, formula_2, orig_vars):
    
