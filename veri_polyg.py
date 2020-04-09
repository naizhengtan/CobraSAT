from z3 import *
import sys
import time

# ====== various encodings =====

# n : integer
# edges : [[i,j], [j,k], ...]
# choice : [ ([[i,j],[j,k],...], [...]), ...   ]
def encode_polyg_tc1(n, edges, constraints):
    print("[TODO] your code here; feel free to modify the function signature")
    assert False


def encode_polyg_tc3(n, edges, constraints):
    print("[TODO] your code here; feel free to modify the function signature")
    assert False


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
            con = []
            for str_group in str_groups:
                group = []
                str_edges = str_group.split(";")
                assert len(str_edges) >= 1, "ill-format constraints, empty constraint"
                for str_edge in str_edges:
                    group.append(extract_edge(str_edge))
                con.append(group)
            constraints.append(con)
        else:
            print("Line = %s" % line)
            assert False, "should never be here"

    return n, edges, constraints


# === main logic ===

def main(encoding, poly_f):
    n, edges, constraints = load_polyg(poly_f)
    print("#nodes=%d" % n)
    print("#edges=%d" % len(edges))
    print("#constraints=%d" % len(constraints))

    #set_option("smt.timeout", 120000) # 120s timeout

    t1 = time.time()

    # (1) encode graph (n, edges, constraints)
    if "tc1" == encoding:
        encode_polyg_tc1(n, edges, constraints)
    elif "tc3" == encoding:
        encode_polyg_tc3(n, edges, constraints)
    else:
        print("ERROR: unknown encoding [%s]. Stop." % encoding)
        return 1
    print("finish construction of clauses")

    t2 = time.time()

    # (2) solve the above encoding
    print("[TODO] your code here; use SMT solvers")

    t3 = time.time()

    print("clause construction: %.fms" % ((t2-t1)*1000))
    print("solve constraints: %.fms" % ((t3-t2)*1000))




def usage_exit():
    print("Usage: veri_polyg.py [tc1|tc3] <polyg_file>")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage_exit()
    main(sys.argv[1], sys.argv[2])

