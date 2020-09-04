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
            num = str(seen[name] if is_positive else -seen[name])
            line.append(num)
        line.append(str(0))
        clause_lines.append(' '.join(line))
    
    return clause_lines, var_count

def to_dimacs(cnf):
    lines = ['c',
             'c dimacs by mike',
             'c']
    
    clause_lines, var_count = make_clause_lines(cnf)

    lines.append(f'p cnf {var_count} {len(clause_lines)}')
    lines.extend(clause_lines)

    return '\n'.join(lines) 