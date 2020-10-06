# CobraSAT

Using SAT/SMT solvers to solve the problem of checking _view_-serializability. 🐍

## Usage

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

## Dependencies

- Python 3.6+
- z3 4.8.9+
- minisat
- monosat
- yices2

You can install from source and place the resulting binary in `.venv/bin` if you are using `venv`.

## Bibliography

- [Cobra: Making Transactional Key-Value Stores Verifiably Serializable (Tan, Zhao, Mu, and Walfish, 2020) (forthcoming)](http://naizhengtan.github.io/)
- [On the Quest for an Acyclic Graph (Janota, Grigore, and Manquinho, 2017)](https://arxiv.org/abs/1708.01745)
- [On the Complexity of Checking Transactional Consistency (Biswas and Enea, 2019)](https://arxiv.org/abs/1908.0450)
- [SAT modulo Graphs: Acyclicity (Gebser, Janhunen, and Rintanen, 2014)](https://link.springer.com/chapter/10.1007/978-3-319-11558-0_10)
