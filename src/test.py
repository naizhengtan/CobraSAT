import unittest
from ser_encodings import ENCODING_CLASSES
from verify import run_encoding
from config import DATA_PATH

class TestEncodings(unittest.TestCase):

    prepend_path = lambda l: map(lambda s: DATA_PATH + '/unit_test/' + s, l)
    unsat_polyg = prepend_path(['cycle.polyg', 'unsat.polyg'])
    sat_polyg = prepend_path(['1cons.polyg', 'rmw.polyg', 'shared_successor.polyg'])

    def test_ser_sat(self):
        for Encoding in ENCODING_CLASSES:
            for polyg in type(self).sat_polyg:
                self.assertTrue(run_encoding(Encoding, polyg))

    def test_ser_unsat(self):
        for Encoding in ENCODING_CLASSES:
            for polyg in type(self).unsat_polyg:
                self.assertFalse(run_encoding(Encoding, polyg))

if __name__ == "__main__":
    unittest.main(buffer=True)
