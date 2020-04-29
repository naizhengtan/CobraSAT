from veri_polyg import load_polyg
import sys
import time

class CNFBuilder:

    def __init__(self):
        self.vars = {}
        self.var_num = 1
        self.clauses = []

    def Bool(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            self.vars[name] = self.var_num
            self.var_num += 1
            return self.vars[name]
    
    def Implies(self, var1, var2):
        return self.Or(self.Not(var1), var2)

    def Or(self, *args):
        return [*args]
    
    def append_Xor(self, var1, var2):
        # xor is associative
        self.clauses.append(Or(Not(var1), Not(var2)))
        self.clauses.append(Or(var1, var2))

    def append(self, or_clause):
        if isinstance(or_clause, list):
            self.clauses.append(or_clause)
        else:
            self.clauses.append([or_clause])

    def Not(self, var):
        return -var
    
    def __str__(self):
        return self.serialize()
    
    def serialize(self):
        lines = ['c',
                 'c generated by mike',
                 'c']
        lines.append('p cnf ' + str(len(self.vars)) + ' ' + str(len(self.clauses)))
        for clause in self.clauses:
            lines.append(' '.join([str(c) for c in clause]) + ' 0')
        
        return '\n'.join(lines)
    
    def aliases(self):
        return (self.Bool, self.Not, self.Or, self.Implies)

def AndImplies(b, var1, var2, var3):
    Bool, Not, Or, Implies = b.aliases() 
    # https://www.wolframalpha.com/input/?i=+CNF+%28%28a+and+b%29+implies+c%29
    # (A and B) implies C
    return Or(Not(var1), Not(var2), var3)

def simple_cnf():
    # test from: https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html
    b = CNFBuilder()
    Bool, Not, Or, Implies = b.aliases()
    
    Bool('x1')
    Bool('x2')
    Bool('x3')

    b.append(Or(Bool('x1'), Not(Bool('x3'))))
    b.append(Or(Bool('x2'), Bool('x3'), Not(Bool('x1'))))

    print(str(b))

    print('Expected:')
    print('''p cnf 3 2
1 -3 0
2 3 -1 0''')

vars = []
vars_aux = []

def generate_vars(n, b):
    global vars, vars_aux
    Bool, Not, Or, Implies = b.aliases()
    print("generating variables...")
    vars = [[Bool(label([i, j])) for i in range(n)] for j in range(n)] 
    vars_aux = [[Bool(label_aux([i, j])) for i in range(n)] for j in range(n)]
    print("done generating variables.")

def var(edge):
    return vars[edge[0]][edge[1]]

def aux(edge):
    return vars_aux[edge[0]][edge[1]]

def label(edge):
    # be careful of slow str ops; 
    # could just label e1, e2 ... (hard to lookup with constraints tho)
    return ','.join([str(e) for e in edge])

def label_aux(edge):
    return 'a' + label(edge)

def polygraph_sat(n, edges, constraints, b): 
    for edge in edges:
        b.append(var(edge))

    for constraint in constraints:
        b.append_Xor(var(constraint[0]), 
                     var(constraint[1]))

def encode_polyg_tc1(n, edges, constraints, b):
    Bool, Not, Or, Implies = b.aliases()

    for begin in range(n):
        b.append(Not(aux([begin, begin])))                             # 1) irreflexive
        for end in range(n):
            b.append(Implies(var([begin, end]), aux([begin, end])))    # 3) closure of edges
            for mid in range(n):
                clause = AndImplies(b, aux([begin, mid]), aux([mid, end]), aux([begin, end]))
                b.append(clause)                                       # 2) transitive
        print('\r{:.2f}%'.format(begin / n), end='')
    print('\n')

def main(encoding, poly_f, output_file):
    n, edges, constraints = load_polyg(poly_f)

    t1 = time.time()

    b = CNFBuilder()
    generate_vars(n, b)

    print('encoding...')    
    if encoding == 'tc1':
        encode_polyg_tc1(n, edges, constraints, b)
    
    t2 = time.time()
    print("clause construction: %.fms" % ((t2-t1)*1000))

    print('writing...')  
    with open(output_file, 'w') as f:
        f.write(str(b))
    
    print('done.')

def usage_exit():
    print("Usage: veri_polyg.py [tc1|tc3] <polyg_file>")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage_exit()
    if len(sys.argv) == 4:
        output_file = sys.argv[3]
    main(sys.argv[1], sys.argv[2], output_file)