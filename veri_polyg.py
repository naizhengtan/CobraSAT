from z3 import *
import monosat
import sys
import time
import math

# from multiprocessing import Pool, cpu_count

# ====== various encodings =====

# TODO: abstract into a higher level interface

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
    vars = [[Bool(label([begin, end])) for end in range(n)] for begin in range(n)]
    vars_aux = [[Bool(label_aux([begin, end])) for end in range(n)] for begin in range(n)]
    print("done generating variables.")

def generate_vars_binary(n):
    global vars, vars_aux
    print("generating variables...")
    vars = [[Bool(label([begin, end])) for end in range(n)] for begin in range(n)]
    vars_aux = [BitVec(','.join(['a', str(i)]), int(math.ceil(math.log2(n)))) for i in range(n)]
    print("done generating variables.")

def var(edge):
    return vars[edge[0]][edge[1]]

def aux(edge):
    return vars_aux[edge[0]][edge[1]]

def aux_binary(i):
    return vars_aux[i]

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

def encode_polyg_unary(n, edges, constraints, s):
    # auxilary variables aux([num_y, num_element]), note that y_i has n-1 elements
    for begin in range(n):
        for end in range(n):
            # s.add(Implies(var([begin, end]), less(begin, end, n)))
            s.add(Implies(var([begin, end]), less(begin, end, n)))
            s.add(unary(begin, n))
        print('\r{:.2f}%'.format(begin / n), end='')
    print('\n')

def unary(ya, n):
    is_unary = True

    for i in range(1, n-1):
        y_i = aux([ya, i])
        y_prev = aux([ya, i-1])
        is_unary = And(is_unary, Implies(y_prev, y_i))

    return is_unary

def less(ya, yb, n):
    u = [Bool(','.join(['u', str(ya), str(yb), str(i)])) for i in range(n-1)]
    return Exists(u, lessunr(ya, yb, u, n))

def lessunr(ya, yb, u, n):
    # ya, yb are indices into aux([ya, element])
    unary_compare = True
    u_nonzero = False

    for i in range(n-1):
        y_i = aux([ya, i])
        z_i = aux([yb, i])
        u_i = u[i]
        # u_i = Bool(','.join(['u', str(ya), str(yb), str(i)]))

        unary_compare_partial = And(Or(Not(y_i), Not(u_i)), Or(z_i, Not(u_i)))
        unary_compare = And(unary_compare, unary_compare_partial)

        u_nonzero = Or(u_nonzero, u_i)

    return And(unary_compare, u_nonzero)

def encode_polyg_topo(n, edges, constraints, s):
    for begin in range(n):
       for end in range(n):
           if begin != end:
               # could we use total linear order instead?
               s.add(Implies(var([begin, end]), \
                             ULT(aux_binary(begin), aux_binary(end))))

def encode_polyg_transitive(n, edges, constraints, s):
    # Buggy! There's a bug in z3 with transitive closures
    # https://theory.stanford.edu/~nikolaj/programmingz3.html#sec-transitive-closure
    # Irreflexive transitive closure => no cycles
    # A = DeclareSort()
    Ints = IntSort()
    Bools = BoolSort()
    R = Function('R', Ints, Ints, Bools) # i R j = Bool
    TC_R = TransitiveClosure(R)

    for begin in range(n):
        s.add(Not(TC_R(begin, begin))) # irreflexive
        for end in range(n):
            s.add(Implies(var([begin, end]), R(begin, end))) # inclusive of all (see 3.1)
            # if begin != end: # this doesnt work; why?
            #     s.add(Implies(var([begin, end]), R(begin, end)))

# probably >= topo time since we aren't able to precompute leaves
def encode_polyg_tree(n, edges, constraints, s):
    # can we get more info about possible leaf nodes by constraints?
    for begin in range(n):
        at_least_one = False
        is_leaf = False

        s.add(Not(var([begin, begin])))
        s.add(UGE(aux_binary(begin), 0))
        s.add(ULE(aux_binary(begin), n - 1))

        for end in range(n):
            # If there is an edge from begin to end, it is not a leaf
            is_leaf = And(Not(var([begin, end])), is_leaf)
            # s.add(Implies(var([begin, end]), UGT(aux_binary(begin), 0)))

            # dist_to_leaf(begin) > dist_to_leaf(end)
            s.add(Implies(var([begin, end]), UGT(aux_binary(begin), aux_binary(end))))

            # at least one is k - 1
            at_least_one = Or(at_least_one, Implies(var([begin, end]), aux_binary(end) == (aux_binary(begin) - 1)))

        s.add(Implies(is_leaf, aux_binary(begin) == 0))
        s.add(at_least_one)


def encode_polyg_be19(n, edges, constraints, s):
    # require WR edges
    for edge in edges:
        s.add(var(edge))
    # CO = Function('WR', Ints, Ints, Bools) # Commit Order

    # encode the polyg constraints in a different way here
    # each constraint option (i, k), (k, j) is a i wr(x) j, k writes x relation
    for constraint in constraints:
        t1 = constraint[1][1]
        t2 = constraint[0][1]
        t3 = constraint[0][0]

        assert t2 == constraint[1][0]

        # s.add(Implies(aux_binary(t2) < aux_binary(t3), aux_binary(t2) < aux_binary(t1))
        # could also use the relation theories (probably not as good)
        # s.add(Implies(CO(t2, t3), CO(t2, t1)))
        s.add(Implies(var([t2, t3]), var([t2, t1])))

    # careful: can't actually use topo here cause that does not imply total order of CO i think
    # since the topo => acyclic, and we no longer have the constraints!
    # could we use integer theories somehow?
    # what about the total linear order?
    for begin in range(n):
        for end in range(n):
            if begin != end:
                s.add(Xor(var([begin, end]), var([end, begin]))) # strcit total order
                for middle in range(n):
                    if begin != middle and end != middle:
                        s.add(Implies(And(var([begin, middle]), var([middle, end])), var([begin, end])))

def encode_polyg_betop(n, edges, constraints, s):
    CO = LinearOrder(IntSort(), 0)

    for edge in edges:
        s.add(CO(edge[0], edge[1]))

    # encode the polyg constraints in a different way here
    # each constraint option (i, k), (k, j) is a i wr(x) j, k writes x relation
    for constraint in constraints:
        t1 = constraint[1][1]
        t2 = constraint[0][1]
        t3 = constraint[0][0]

        assert t2 == constraint[1][0]
        s.add(Implies(CO(t2, t3), CO(t2, t1)))

    for begin in range(n):
        for end in range(n):
            if begin != end:
                s.add(Xor(CO(begin, end), CO(end, begin))) # strcit total order


def polyg_monosat(n, edges, constraints):
    monosat.Monosat().newSolver()
    graph = monosat.Graph()

    for i in range(n):
        graph.addNode()

    for edge in edges:
        edge = graph.addEdge(*edge)
        monosat.Assert(edge)

    for constraint in constraints:
        e1 = graph.addEdge(*(constraint[0]))
        e2 = graph.addEdge(*(constraint[1]))
        monosat.Assert(monosat.And(monosat.Or(e1, e2), \
                                   monosat.Or(monosat.Not(e1), \
                                              monosat.Not(e2))))

    monosat.Assert(graph.acyclic())
    result = monosat.Solve()

    if result:
        print("sat")
    else:
        print("unsat")

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


    if "monosat" == encoding:
        polyg_monosat(n, edges, constraints)
        exit()

    #set_option("smt.timeout", 120000) # 120s timeout

    t1 = time.time()

    s = Solver()

    # (1) encode graph (n, edges, constraints)
    # should prolly move generate_vars and polygraph_sat into the encoding
    # functions for encapsulation
    if "tc1" == encoding:
        generate_vars(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_tc1(n, edges, constraints, s)
    elif "tc3" == encoding:
        generate_vars(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_tc3(n, edges, constraints, s)
    elif "unr" == encoding:
        generate_vars(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_unary(n, edges, constraints, s)
    elif "top" == encoding:
        generate_vars_binary(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_topo(n, edges, constraints, s)
    elif "tc" == encoding:
        generate_vars(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_transitive(n, edges, constraints, s)
    elif "tree" == encoding:
        generate_vars_binary(n)
        polygraph_sat(n, edges, constraints, s)
        encode_polyg_tree(n, edges, constraints, s)
    elif "be19" == encoding:
        generate_vars(n)
        # don't need polygraph sat here.
        encode_polyg_be19(n, edges, constraints, s)
    elif "betop" == encoding:
        generate_vars_binary(n)
        encode_polyg_betop(n, edges, constraints, s)
    else:
        print("ERROR: unknown encoding [%s]. Stop." % encoding)
        return 1

    t2 = time.time()
    print("clause construction: %.fms" % ((t2-t1)*1000))

    # (2) solve the above encoding
    if output_file:
        print("writing to file: " + output_file)
        with open(output_file, 'w') as f:
            # there also exists: http://z3prover.github.io/api/html/z3py_8py_source.html#l06889
            # s.dimacs() -> but not sure if this is advised?
            f.write(s.to_smt2())
        t3 = time.time()
        print("write to file: %.fms" % ((t3-t2)*1000))
    else:
        print(s.check())
        t3 = time.time()
        print("solve constraints: %.fms" % ((t3-t2)*1000))
        # for debugging:
        print(s.model())


def usage_exit():
    print("Usage: veri_polyg.py [tc1|tc3|unr|top|tc|tree] <polyg_file>")
    exit(1)

if __name__ == "__main__":
    output_file = ''
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage_exit()
    if len(sys.argv) == 4:
        output_file = sys.argv[3]
    main(sys.argv[1], sys.argv[2], output_file)

