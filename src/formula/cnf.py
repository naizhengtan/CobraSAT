# cnf is a list of clauses
# clause is a tuple of literals
# literal is (name: str, pos: bool)

# dimacs:
# top can have comment lines, start with c
# problem line: p cnf <vars> <clauses>
# clause line: <int> <int> ... 0
# where int is the var number, and -i as NOT(ith var)

def and_cnf(left_cnf, right_cnf):
    return left_cnf + right_cnf

def clause(literals):
    return [...literals] 

def lit(name, is_positive=True):
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
                simplified.append(lit(name, is_positive))
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