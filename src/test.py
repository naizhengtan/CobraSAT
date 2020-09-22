import unittest

from ser_encodings import (
    ENCODING_CLASSES,
    TC1, TC3, TC,
    TopoBitVec, TopoInt,
    Axiomatic,
    Mono,
    TreeBV,
    BinaryLabelMinisat, BinaryLabelZ3,
    UnaryLabel
)

from verify import run_encoding
from config import DATA_PATH, PROJECT_ROOT
import os
from contextlib import redirect_stdout
from io import StringIO


# due to map returning an iterator, we have to convert to list for it to be reused
prepend_path = lambda l: list(map(lambda s: DATA_PATH + '/unit_test/' + s, l))
unsat_polyg = prepend_path(['cycle.polyg', 'unsat.polyg'])
sat_polyg = prepend_path(['1cons.polyg', 'rmw.polyg', 'shared_successor.polyg'])

def assert_sat(test, Encoding):
    for polyg in sat_polyg:
        with test.subTest(polyg=polyg):
            result, enc = run_encoding(Encoding, polyg)
            test.assertTrue(result)

def assert_unsat(test, Encoding):
    for polyg in unsat_polyg:
        with test.subTest(polyg=polyg):
            result, enc = run_encoding(Encoding, polyg)
            test.assertFalse(result)

# prefer to test individually to avoid errors
def assert_ser(test, Encoding):
    assert_sat(test, Encoding)
    assert_unsat(test, Encoding)

class TestEncodings(unittest.TestCase):
    def test_tc1(self):
        assert_ser(self, TC1)

    def test_tc3(self):
        assert_ser(self, TC3)

    def test_tc(self):
        assert_ser(self, TC)

    def test_topo_bitvec(self):
        assert_ser(self, TopoBitVec)

    def test_topo_int(self):
        assert_ser(self, TopoInt)

    def test_axiomatic(self):
        assert_ser(self, Axiomatic)

    def test_mono(self):
        assert_ser(self, Mono)

    def test_tree_bitvec(self):
        assert_ser(self, TreeBV)

    def test_writes(self):
        for polyg in sat_polyg:
            run_encoding(BinaryLabelMinisat, polyg) 
            run_encoding(UnaryLabel, polyg) 

            self.assertTrue(os.path.isfile(PROJECT_ROOT + '/dimacs/binary-label.dimacs'))
            self.assertTrue(os.path.isfile(PROJECT_ROOT + '/dimacs/unary-label.dimacs'))

class TestDimacsEncodings(unittest.TestCase):
    def test_binary_label(self):
        assert_ser(self, BinaryLabelMinisat)
        assert_ser(self, BinaryLabelZ3)

    def test_unary_label(self):
        assert_ser(self, UnaryLabel)

if __name__ == "__main__":
    # hide stdout, even on failure
    # https://codingdose.info/2018/03/22/supress-print-output-in-python/
    trap = StringIO()
    with redirect_stdout(trap):
        unittest.main()
