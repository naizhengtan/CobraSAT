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
    simplified = []

    for clause in cnf:
        simplified_clause = simplify_clause(clause)
        if simplified_clause:
            simplified.append(simplified_clause)
    
    return simplified

def simplify_clause(clause):
    # simple rules:
    # Normalize !TRUE and !FALSE to FALSE and TRUE
    # 1. if TRUE in clause then remove clause
    # 2. if clause has both Var and !Var, remove clause
    # 3. remove FALSE from clauses
    
    seen = {} # let seen[Var] = True mean positive literal seen
    for literal in clause:
        name, is_positive = literal
        simplified = []

        # rules 1 and 2
        if is_true_literal(literal) and not (name in seen and seen[name] != is_positive):
            # rule 3
            if not is_false_literal(literal): 
                simplified.append(literal(name, is_positive))
                seen[name] = is_positive
        else:
            return []
     
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
    def __init__(self, literals=[]):
        self.literals = literals
    
    def or_clause(self, clause):
        assert isinstance(clause, Clause)
        self.literals.extend(clause.literals)
        return self
    
    def __iter__(self):
        return iter(self.literals)
    
    def __repr__(self):
        return f'({" OR ".join([literal_to_str(literal) for literal in self])})'

def and_cnfs(cnf_1, cnf_2):
    return CNF(cnf_1.clauses + cnf_2.clauses)

def or_clauses(clause_1, clause_2):
    return Clause(clause_1.literals + clause_2.literals)

def literal_to_str(literal):
    name, is_positive = literal
    sign = '' if is_positive else '~'
    return f'{sign}{name}'