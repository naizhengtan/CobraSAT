from abc import ABC, abstractmethod

class Encoding(ABC):
    @abstractmethod
    def __init__(self, total_nodes):
        pass

    @abstractmethod
    def encode(self, total_nodes, edges, constraints, **options):
        pass

    @abstractmethod
    def solve(self):
        results = self.solver.check()
        if repr(results) == 'sat':
            return True
        elif repr(results) == 'unsat':
            return False
        else:
            raise Exception("Unknown SAT result")

    @property
    def filetype(self):
        return None

    def write_to_file(self):
        raise Exception("This encoding does not support writing to file")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    def print_progresss(self):
        pass