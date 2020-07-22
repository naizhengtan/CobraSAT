from veri_polyg import load_polyg
import time
from ser_encodings.tc1 import TC1

class Stopwatch:
    def __init__(self):
        self.start_time = time.time()

    def stop_and_start(self):
        diff = time.time() - self.start_time()
        self.start_time = time.time()
        return diff

def timing(start, end):
    return (end - start)


def run_encoding(Encoding, polyg_filename):
    print('encoding: ' + Encoding.__name__)
    print('description: ' + Encoding.description)
    print('polygraph: ' + polyg_filename)
    print('loading polygraph...')
    n, edges, constraints = load_polyg(polyg_filename)

    print('\ninitialize encoding...')
    start = time.time()

    enc = Encoding(n)
    init_done = time.time()
    print("init: {:.6f}sec".format(timing(start, init_done)))

    print('\nbuilding encoding...')
    enc.encode(edges, constraints)
    encode_done = time.time()
    print("encode: {:.6f}sec".format(timing(init_done, encode_done)))

    print('\nbuilding encoding...')
    results = enc.solve()
    solve_done = time.time()
    print("solve: {:.6f}sec".format(timing(encode_done, solve_done)))

    print("\nsat? " + str(results))

    return results


def main():
    encodings = [TC1]

    for Encoding in encodings:
        run_encoding(Encoding, '../polygraphs/unit_test/cycle.polyg')


if __name__ == "__main__":
    main()
