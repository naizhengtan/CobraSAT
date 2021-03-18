# CobraSAT

Using SAT/SMT solvers to check serializability of _black-box_ databases. 🐍

## About

This project compares the performance of different SAT/SMT encodings
and solvers for verifying the serializability of black-box databases.

Our motivation is to understand how different encodings and solvers influence the verification performance.
In particular,
we experiment with existing SAT/SMT encodings and widely used solvers
under transaction history workloads for verifying serializability (see [[1]](#cobra)).

## Experiments

We evaluated existing serializability encodings (or polygraph acyclicity encoding, see section 2.3 [[1]](#cobra)), including: 
- SAT binary labeling encoding, using Tseitin's transformation for encoding lexographic ordering [[2]](#cite2)
  - Z3 (`*-z3`), Yices2 (`*-yices2`), and MiniSAT (`*-minisat`).
- SAT unary labeling encoding [[2]](#cite2)
  - Z3 (`*-z3`), Yices2 (`*-yices2`), and MiniSAT (`*-minisat`).
- Transitive closure encoding (`tc1`, `tc3`) [[2]](#cite2). 
  - `tc` was encoded directly using Z3's `TransitiveClosure` relation [[6]](#z3).
- SMT topological ordering encoding [[3]](#cite3).
  - `topo-bv` was using Z3's `BitVec` variables, and `topo-int` was using Z3's `Int` variables [[6]](#z3).
- Tree reduction encoding [[3]](#cite3)
- Serializability consistency axioms (`axiom`) of database history [[4]](#cite4).
- Direct MonoSAT encoding (`mono`) [[5]](#monosat).

We ran the experiments on a benchmark with different ratios of random read-only and write-only transactions (see details in section 6 of paper [[1]](#cobra)). The read:write ratio workloads tested were 50:50, 75:25, and 90:10. The workloads are given as polygraph files (`.polyg`) consisting of node counts, edges, and constraints. Nodes correspond to transactions, and edges as write-read dependencies. Writes have been combined to reduce constraints in the polygraph (see section 2.3 and 3.1 of Cobra paper [[1]](#cobra)).

Binary and unary labeling encodings were first compiled into DIMACS files by Python before being passed into solvers. `mono` was encoded directly into MonoSAT Python. All others were encoded directly into Z3 Python.

## Results

*For full graphs, see `exploration.ipynb`. Raw data is in `final.pckl`.*

### How do different encodings and solvers perform? How does runtime grow with larger workloads?

<!---
####  Plot of log of total runtime against number of nodes for 50:50 read-write ratio polygraphs
-->

Figure below depicts the increase in total verification time against number of nodes, for 50:50 read-write ratio workloads.

![Plot of runtime against number of nodes for 50:50 read-write ratio polygraphs](images/runtime-against-nodes.png)


Runtime tends to grow exponentially with respect to node counts. `mono` is the clear performance winner, running significantly faster than all other encoding/solver pairs. The next fastest are `tc`, `topo-bv`, and `topo-int`, notably implemented most directly with Z3's higher level theories. `tree-bv` scales poorly with node count.
Note that \*tree-bv for node counts over 200 excluded because of timeouts.

### How do different solvers perform with the same encoding?


<!--
#### Plot of runtime against number of nodes for 75:25 read-write ratio polygraphs, comparing solver backends
-->

We compare different solver backends (Z3, MiniSAT, and Yices2) with the same encodings (binary and unary labeling) for the same workload (75:25 read-write ratio workload), and the results are as follows.


![Plot of runtime against number of nodes for 75:25 read-write ratio polygraphs, comparing solver backends](images/backend-comparison.png)

Different encodings tend to perform similarly for different solvers. However, Yices2 scales much more effectively as node count grows for unary labeling.

### What's the relationship between the number of SAT/SMT variables of an encoding and its solving time? 

We define variables in the standard way for SAT and as Z3 variables for SMT,
and plot the number of variables in each encoding with their verification time in the figure below.

<!--
#### Plot of log solve time against number of SAT variables for all polygraphs
-->


![Plot of solve time against number of variables for all polygraphs](images/solve-time-against-variables.png)

We can see from the plot that greater variable counts correlates with greater solve times, even when comparing encodings.
Note that for this graph only, `binary-label-minisat` and `unary-label-minisat` include all binary labeling and unary labeling solvers, not just MiniSAT.


## Dependencies

- Python 3.6+
- z3 4.8.9+
- minisat
- monosat
- yices2

You can install from source and place the resulting binary in `.venv/bin` if you are using `venv`.

## Usage (reproduce our results)

Use `verify.py` to solve a given polygraph with a given encoding.

```
> python src/verify.py --help
```

Use `experiments.py` run the experiments, solving all the polygraphs in `polygraphs/workloads3` with every available encoding. The results are stored in the `results.pckl` [Pickle](https://docs.python.org/3/library/pickle.html) file as a dictionary.
```
> python src/experiments.py
```

To run the test suite:
```
> python src/test.py
```


## Bibliography

- <a name='cobra'></a>[1] [Cobra: Making Transactional Key-Value Stores Verifiably Serializable (Tan, Zhao, Mu, and Walfish, 2020)](http://naizhengtan.github.io/doc/papers/cobra20tan.pdf)
- <a name='cite2'></a>[2] [On the Quest for an Acyclic Graph (Janota, Grigore, and Manquinho, 2017)](https://arxiv.org/abs/1708.01745)
- <a name='cite3'></a>[3] [SAT modulo Graphs: Acyclicity (Gebser, Janhunen, and Rintanen, 2014)](https://link.springer.com/chapter/10.1007/978-3-319-11558-0_10)
- <a name='cite4'></a>[4] [On the Complexity of Checking Transactional Consistency (Biswas and Enea, 2019)](https://arxiv.org/abs/1908.0450)
- <a name='monosat'></a>[5] [SAT Modulo Monotonic Theories (Bayless, Bayless, Hoos, and Hu, 2015)](http://www.cs.ubc.ca/labs/isd/Projects/monosat/smmt.pdf)
- <a name='z3'></a>[6] [Z3: An Efficient SMT Solver (de Moura and Bjørner, 2008)](https://link.springer.com/content/pdf/10.1007%2F978-3-540-78800-3_24.pdf)

