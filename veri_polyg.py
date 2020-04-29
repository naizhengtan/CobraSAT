from z3 import *
import sys
import time

from multiprocessing import Pool, cpu_count

# ====== various encodings =====

vars = []
vars_aux = []

def polygraph_sat(n, edges, constraints, s): 
    # maybe should just return a list?
    # requires all edges of known RW
    for edge in edges:
        s.add(var(edge))

    # requires one but not both of constraints to be satisfied
    # actually, this is between two groups (either must be true)
    # must revert the encoding
    for constraint in constraints:
        s.add(Xor(var(constraint[0]), 
                  var(constraint[1])))


def generate_vars(n):
    global vars, vars_aux
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

def encode_polyg_tc1(n, edges, constraints, s):
    # can't just iterate edges due to constraints also being a possibility as an edge
    for begin in range(n):
        s.add(Not(aux([begin, begin])))                             # 1) irreflexive
        for end in range(n):
            s.add(Implies(var([begin, end]), aux([begin, end])))    # 3) closure of edges
            for mid in range(n):
                connecting = And(aux([begin, mid]), 
                                  aux([mid, end]))
                s.add(Implies(connecting, aux([begin, end])))       # 2) transitive
        print('\r{:.2f}%'.format(begin / n), end='')
    print('\n')


def encode_polyg_tc3(n, edges, constraints, s):
    for begin in range(n):
        s.add(Not(var([begin, begin])))
        for end in range(n):
            for mid in range(n):
                connecting = And(var([begin, mid]), var([mid, end]))
                s.add(Implies(connecting, var([begin, end])))
        print('\r{:.2f}%'.format(begin / n), end='')
    print('\n')

# ====== load file =====

def extract_edge(edge):
    tokens = edge.split(",")
    assert len(tokens) == 2, "ill-format edge: a,b"
    return [int(tokens[0]), int(tokens[1])]


def load_polyg(poly_f):
    with open(poly_f) as f:
        lines = f.readlines()

    n = 0
    edges = []
    constraints = []
    for line in lines:
        if line == "":
            continue

        elems = line.split(':')
        assert len(elems) == 2, "ill-format log"
        symbol = elems[0]
        content = elems[1]

        if symbol == "n":
            assert n==0, "multiple n in file"
            n = int(content)
        elif symbol == "e":
            e = extract_edge(content)
            edges.append(e)
        elif symbol == "c":
            str_groups = content.split("|")
            assert len(str_groups) == 2, "ill-format constraints, not two groups"
            con = [[int(g) for g in group.split(',')] for group in str_groups]
            constraints.append(con)
        else:
            print("Line = %s" % line)
            assert False, "should never be here"

    return n, edges, constraints


# === main logic ===

def main(encoding, poly_f, output_file):
    set_param('parallel.enable', True)
    set_param('parallel.threads.max', 4)
    
    n, edges, constraints = load_polyg(poly_f)
    print("#nodes=%d" % n)
    print("#edges=%d" % len(edges))
    print("#constraints=%d" % len(constraints))

    #set_option("smt.timeout", 120000) # 120s timeout

    t1 = time.time()
        
    s = Solver()

    generate_vars(n)
    polygraph_sat(n, edges, constraints, s)

    # (1) encode graph (n, edges, constraints)
    if "tc1" == encoding:
        encode_polyg_tc1(n, edges, constraints, s)
    elif "tc3" == encoding:
        encode_polyg_tc3(n, edges, constraints, s)
    else:
        print("ERROR: unknown encoding [%s]. Stop." % encoding)
        return 1
    # print("finish construction of clauses")

    t2 = time.time()
    print("clause construction: %.fms" % ((t2-t1)*1000))

    # (2) solve the above encoding
    if output_file:
        print("writing to file: " + output_file)
        with open(output_file, 'w') as f:
            f.write(s.to_smt2())
        t3 = time.time()
        print("write to file: %.fms" % ((t3-t2)*1000))
    else:
        print(s.check())
        t3 = time.time()
        print("solve constraints: %.fms" % ((t3-t2)*1000))


def usage_exit():
    print("Usage: veri_polyg.py [tc1|tc3] <polyg_file>")
    exit(1)

if __name__ == "__main__": 
    output_file = ''
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage_exit()
    if len(sys.argv) == 4:
        output_file = sys.argv[3]
    main(sys.argv[1], sys.argv[2], output_file)

