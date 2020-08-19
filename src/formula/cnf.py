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
    # 1. if TRUE in clause then remove clause
    # 2. if clause has both Var and !Var, remove clause
    # 3. remove FALSE from clauses
    
    seen = {} # let seen[Var] = True mean positive literal seen
    for literal in clause:
        name, is_positive = literal
        simplified = []

        # rules 1 and 2
        if is_true_literal(literal) and !(name in seen and seen[name] != is_positive):
            # rule 3
            if not is_false_literal(literal): 
                simplified.append(literal(name, is_positive))
                seen[name] = is_positive
        else:
            return []
     
    return simplified

def is_true_literal(literal):
    return literal == ('TRUE', True) or literal == ('FALSE', False)

def is_false_literal(literal):
    return literal == ('FALSE', True) or literal == ('TRUE', False)

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
    def __init__(self, clauses=[]):
        self.clauses = clauses
    
    def and_cnf(self, cnf):
        self.clauses.append(clause)
        return self
    
    def __iter__(self):
        return self.clauses
    
class Clause:
    def __init__(self, literals=[]):
        self.literals = literals
    
    def add_literal(self, literal):
        self.literals.append(literal)

    def or_clause(self, clause):
        self.literals.extend(clause.literals)
        return self
    
    def __iter__(self):
        return self.literals
    
class Literal:
    def __init__(self, name, positive=True):
        self.name = name
        self.positive = positive
    
    def __eq__(self, literal):
        same_name = self.name == literal.name

def negated(literal):
    return Literal(literal.name, not literal.positive)

# class TrueAtom(Literal):
#     def __init__(self):
#         super().__init__('TRUE', True)
    
#     def __eq__(self, literal):
#         is_true = literal.name == 'TRUE' and literal.positive
#         is_neg_false = negated(literal) == FalseAtom()
#         return is_true or is_neg_false

# class FalseAtom(Literal):
#     def __init__(self):
#         super().__init__('FALSE', True)

#     def __eq__(self, literal):
#         is_false = literal.name == 'FALSE' and literal.positive
#         is_neg_true = negated(literal) == TrueAtom()
#         return is_false or is_neg_true