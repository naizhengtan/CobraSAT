from veri_polyg import load_polyg
import sys
import time

from CNFBuilder import *

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
        print('\r{:.2f}%'.format(begin / n * 100), end='')
    print('\n')

def encode_polyg_tc3(n, edges, constraints, b):
    Bool, Not, Or, Implies = b.aliases()

    for begin in range(n):
        b.append(Not(var([begin, begin])))                             # 1) irreflexive and closure
        for end in range(n):
            for mid in range(n):
                clause = AndImplies(b, var([begin, mid]), var([mid, end]), var([begin, end]))
                b.append(clause)                                       # 2) transitive
        print('\r{:.2f}%'.format(begin / n * 100), end='')
    print('\n')

# def encode_polyg_unary(n, edges, constraints, b):
#     # https://april.eecs.umich.edu/courses/eecs492_w10/wiki/images/6/6b/CNF_conversion.pdf
#     Bool, Not, Or, Implies = b.aliases()

#     for begin in range(n):
#         for end in range(n):

def encode_polyg_be19(n, edges, constraints, s):
    Bool, Not, Or, Implies = s.aliases()

    for constraint in constraints:
        t1 = constraint[1][1]
        t2 = constraint[0][1]
        t3 = constraint[0][0]

        s.append(Implies(var([t2, t3]), var([t2, t1])))

    for begin in range(n):
        for end in range(n):
            if begin != end:
                s.append_Xor(var([begin, end]), var([end, begin])) # strcit total order
                for middle in range(n):
                    if begin != middle and end != middle:
                        clause = AndImplies(s, var([begin, middle]), var([middle, end]), var([begin, end]))
                        s.append(clause)

def main(encoding, poly_f, output_file):
    n, edges, constraints = load_polyg(poly_f)

    t1 = time.time()

    b = CNFBuilder()
    generate_vars(n, b)

    polygraph_sat(n, edges, constraints, b)

    print('encoding...')
    if encoding == 'tc1':
        encode_polyg_tc1(n, edges, constraints, b)
    elif encoding == 'tc3':
        encode_polyg_tc3(n, edges, constraints, b)
    elif encoding == 'be19':
        encode_polyg_be19(n, edges, constraints, b)
    else:
        print('not a valid encoding!')
        usage_exit()

    t2 = time.time()
    print("clause construction: %.fms" % ((t2-t1)*1000))

    print('writing...')

    if output_file == 'default':
        output_file = poly_f.split('.')[0] + encoding + '.cnf'

    with open(output_file, 'w') as f:
        f.write(str(b))

    t3 = time.time()
    print("write to cnf: %.fms" % ((t3-t2)*1000))
    print('done.')

def usage_exit():
    print("Usage: build_cnf.py [tc1|tc3|be19] <polyg_file> <cnf_file>")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) <= 3 and len(sys.argv) != 4:
        usage_exit()
    if len(sys.argv) == 4:
        output_file = sys.argv[3]
    main(sys.argv[1], sys.argv[2], output_file)
