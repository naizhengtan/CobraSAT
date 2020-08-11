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

def lit(name, positive=True):
    return (name, positive)

def make_clause_lines(cnf):
    seen = {}
    var_count = 0
    clause_lines = []

    for clause in cnf:
        line = []
        for name, positive in clause:
            if name not in seen:
                var_count += 1
                seen[name] = var_count
            num = seen[name] if positive else -seen[name]
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