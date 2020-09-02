# cnf is a list of clauses
# clause is a list of literals
# literal is (name: str, pos: bool)

# dimacs:
# top can have comment lines, start with c
# problem line: p cnf <vars> <clauses>
# clause line: <int> <int> ... 0
# where int is the var number, and -i as NOT(ith var)

def literal(name, is_positive=True):
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
    for literal in clause:
        simplified = Clause()
        name, is_positive = literal
        is_tf = name == 'TRUE' or name == 'FALSE'

        # Normalize True and False
        if is_tf and not is_positive:
            literal = ('TRUE' if name == 'FALSE' else 'FALSE', True)

        if name in seen:
            if is_positive != seen[name]: # both Var, !Var are in clause => clause is always true
                return []
        else:
            simplified.add_literal(literal)
            seen[name] = is_positive
     
    return simplified

def TRUE():
    return ('TRUE', True)

def FALSE():
    return ('FALSE', False)

def normalize_literal(literal):
    name, is_positive = literal
    is_const = name is 'TRUE' or name is 'FALSE'
    if is_const and not is_positive:
        return (name, not is_positive)
    else:
        return literal

def make_clause_lines(cnf):
    seen = {}
    var_count = 0
    clause_lines = []

    for clause in cnf:
        line = []
        for name, is_positive in clause:
            if name not in seen:
                var_count += 1
                seen[name] = var_count
            num = seen[name] if is_positive else -seen[name]
            line.append(num)
        line.append(0)
        clause_lines.append(line)
    
    return clause_lines, var_count

def to_dimacs(cnf):
    lines = ['c',
             'c dimacs by mike',
             'c']
    
    clause_lines, var_count = make_clause_lines(cnf)

    lines.append(f'p cnf {var_count} {len(clause_lines)}')
    lines.extend(clause_lines)

    return '\n'.join(lines)

# TODO: should probably just class CNF(list)
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
    
    def __iter__(self):
        return iter(self.clauses)
    
    def __repr__(self):
        return ' AND '.join([str(clause) for clause in self])

class Clause:
    def __init__(self, literals=None):
        if literals is None:
            literals = []
        self.literals = literals
    
    def or_clause(self, clause):
        assert isinstance(clause, Clause)
        self.literals.extend(clause.literals)
        return self
    
    def add_literal(self, literal):
        self.literals.append(literal)

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