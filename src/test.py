import unittest

from ser_encodings import (
    ENCODING_CLASSES,
    TC1, TC3, TC,
    TopoBitVec, TopoInt,
    Axiomatic,
    Mono,
    TreeBV,
    BinaryLabel,
    UnaryLabel
)

from verify import run_encoding
from config import DATA_PATH, PROJECT_ROOT
import os

class TestEncodings(unittest.TestCase):
    # due to map returning an iterator, we have to convert to list for it to be reused
    prepend_path = lambda l: list(map(lambda s: DATA_PATH + '/unit_test/' + s, l))
    unsat_polyg = prepend_path(['cycle.polyg', 'unsat.polyg'])
    sat_polyg = prepend_path(['1cons.polyg', 'rmw.polyg', 'shared_successor.polyg'])

    def assert_sat(self, Encoding):
        for polyg in self.sat_polyg:
            result, enc = run_encoding(Encoding, polyg)
            self.assertTrue(result)

    def assert_unsat(self, Encoding):
        for polyg in self.unsat_polyg:
            print(polyg)
            result, enc = run_encoding(Encoding, polyg)
            self.assertFalse(result)

    # prefer to test individually to avoid errors
    def assert_ser(self, Encoding):
        self.assert_sat(Encoding)
        self.assert_unsat(Encoding)

    def test_tc1(self):
        self.assert_ser(TC1)

    def test_tc3(self):
        self.assert_ser(TC3)

    def test_tc(self):
        self.assert_ser(TC)

    def test_topo_bitvec(self):
        self.assert_ser(TopoBitVec)

    def test_topo_int(self):
        self.assert_ser(TopoInt)

    def test_axiomatic(self):
        self.assert_ser(Axiomatic)

    def test_mono(self):
        self.assert_ser(Mono)

    def test_tree_bitvec(self):
        self.assert_ser(TreeBV)

    def test_writes(self):
        for polyg in self.sat_polyg:
            run_encoding(BinaryLabel, polyg) 
            run_encoding(UnaryLabel, polyg) 

            self.assertTrue(os.path.isfile(PROJECT_ROOT + '/dimacs/binary-label.dimacs'))
            self.assertTrue(os.path.isfile(PROJECT_ROOT + '/dimacs/unary-label.dimacs'))

if __name__ == "__main__":
    unittest.main(buffer=True)
    # unittest.main()
