from formula.formula import *
from formula.cnf import *
from formula.convert import *
from formula.dimacs import *

f = Or(And(Atom('p1'), Atom('q1')), Or(And(Atom('p2'), Not(Atom('q2'))), And(Not(Atom('p3')), Not(Atom('q3')))))
print(f.accept(ToCNF()))
print()

f = Or(And(Atom('p1'), Atom('q1')), Or(And(Atom('p2'), Not(Atom('q2'))), And(Not(Atom('p3')), Not(Atom('q3')))))
print(to_tseitin_cnf(f))
print()

t1, t2, t3 = make_atoms('t1 t2 t3')
q1, q2, q3 = make_atoms('q1 q2 q3')
p1, p2, p3 = make_atoms('p1 p2 p3')

clause1 = Or(t1, Or(t2, t3))
clause2 = Iff(t1, And(p1, q1))
clause3 = Iff(t2, And(p2, Not(q2)))
clause4 = Iff(t3, And(Not(p3), Not(q3)))
f = And(clause1, And(clause2, And(clause3, clause4)))
print(to_cnf(f))
print()

print('a, b, c')
a, b, c = make_atoms('a b c')
f = Iff(a, Not(b))
c = to_cnf(f)
# c = simplify_cnf(to_cnf(f))
print(c)
print()

f = Iff(a, b)
print(to_cnf(f))
print()
# d = to_dimacs(c)
# print(d)

p, q, r = make_atoms('p q r')
f = Not(And(p, Or(q, Not(r))))
print(to_tseitin_cnf(f))

