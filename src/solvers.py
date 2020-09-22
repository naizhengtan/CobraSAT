import subprocess

def minisat_dimacs(dimacs_filename):
    result = subprocess.run(['minisat', dimacs_filename],
                            capture_output=True)
    # 0 if parsing the command line options fails, usage information is requested, 
    # or output of the input problem in DIMACS format succeeds. 
    # 1 if interrupted by SIGINT or if an input file cannot be read, 
    # 3 if parsing the input fails, 
    # 10 if found satisfiable, and 20 if found unsatisfiable. 
    assert result.returncode == 10 or result.returncode == 20

    if result.returncode == 10:
        return True
    else:
        return False

def z3_dimacs(dimacs_filename):
    result = subprocess.run(['z3', '-dimacs', dimacs_filename], capture_output=True)
    output = result.stdout.split()[0]
    print(output)
    assert output == b'unsat' or output == b'sat'

    if output == b'sat':
        return True
    else:
        return False