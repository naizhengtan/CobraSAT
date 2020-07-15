from veri_polyg import load_polyg
import time
from Encoding import TC1

class Stopwatch:
    def __init__(self):
        self.start_time = time.time()

    def stop_and_start(self):
        diff = time.time() - self.start_time()
        self.start_time = time.time()
        return diff

def timing(start, end):
    return (end - start) * 1000


def run_encoding(Encoding, polyg_filename)
    print('loading polygraph...')
    n, edges, constraints = load_polyg(polyg_filename)

    print('initialize encoding...')
    start = time.time()

    enc = Encoding(n)
    init_done = time.time()
    print("init: {:.f}sec".format(timing(start, init_done)))

    print('building encoding...')
    enc.encode(edges, constraints)
    encode_done = time.time()
    print("encode: {:.f}sec".format(timing(init_done, encode_done)))

    print('building encoding...')
    results = enc.solve()
    solve_done = time.time()
    print("solve: {:.f}sec".format(timing(encode_done, solve_done)))

    return results,


def main():
    encodings = [TC1]

    for Encoding in encodings:
        run_encoding(Encoding, 'polygraphs/unit_test/1cons.polyg')


if __name__ == "__main__":
    main()
