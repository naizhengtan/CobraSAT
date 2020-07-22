import argparse
import time
from veri_polyg import load_polyg
from ser_encodings import ENCODING_CLASSES

class Stopwatch:
    def __init__(self):
        self.start_time = time.time()

    def stop_and_start(self):
        diff = time.time() - self.start_time()
        self.start_time = time.time()
        return diff

def timing(start, end):
    return (end - start)


def run_encoding(Encoding, polyg_filename, output_filename=None):
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

    results = None
    if not output_filename:
        print('\nsolving encoding...')
        results = enc.solve()
        solve_done = time.time()
        print("solve: {:.6f}sec".format(timing(encode_done, solve_done)))

        print("\nsat? " + str(results))
    else:
        print('\nwriting encoding to file...')
        # TODO: write to file (and time it)

    return results


def main():
    parser = argparse.ArgumentParser()
    encoding_choices = {}

    for cl in ENCODING_CLASSES:
        if not cl in encoding_choices:
            encoding_choices[cl.name] = cl
        else:
            raise Exception('duplicate encoding names')

    parser.add_argument('encoding', help='encoding to use', choices=encoding_choices)
    parser.add_argument('polygraph', help='polygraph file')
    parser.add_argument('-o', '--output', help='save encoding to file')

    args = parser.parse_args()
    run_encoding(encoding_choices[args.encoding], args.polygraph, args.output)

if __name__ == '__main__':
    main()
