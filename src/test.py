import unittest

from ser_encodings import (
    ENCODING_CLASSES,
    TC1, TC3, TC,
    TopoBitVec, TopoInt,
    Axiomatic,
    Mono
)

from verify import run_encoding
from config import DATA_PATH

class TestEncodings(unittest.TestCase):

    # due to map returning an iterator, we have to convert to list for it to be reused
    prepend_path = lambda l: list(map(lambda s: DATA_PATH + '/unit_test/' + s, l))
    unsat_polyg = prepend_path(['cycle.polyg', 'unsat.polyg'])
    sat_polyg = prepend_path(['1cons.polyg', 'rmw.polyg', 'shared_successor.polyg'])

    def assert_sat(self, Encoding):
        for polyg in type(self).sat_polyg:
            self.assertTrue(run_encoding(Encoding, polyg))

    def assert_unsat(self, Encoding):
        for polyg in type(self).unsat_polyg:
            self.assertFalse(run_encoding(Encoding, polyg))

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
    # prefer to test individually instead to avoid errors
    # def test_ser_sat(self):
    #     for Encoding in ENCODING_CLASSES:
    #         for polyg in type(self).sat_polyg:
    #             self.assertTrue(run_encoding(Encoding, polyg))

    # def test_ser_unsat(self):
    #     for Encoding in ENCODING_CLASSES:
    #         for polyg in type(self).unsat_polyg:
    #             self.assertFalse(run_encoding(Encoding, polyg))

if __name__ == "__main__":
    unittest.main(buffer=True)
