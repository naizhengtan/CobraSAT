import argparse
from argparse import RawDescriptionHelpFormatter
import time
from encoding.polygraph import load_polyg
from serializability import ENCODING_CLASSES

def run_encoding(Encoding, polyg_filename, output_filename=None):
    print('encoding: ' + Encoding.__name__)
    # print('description: ' + Encoding.description)
    print('polygraph: ' + polyg_filename)
    print('loading polygraph...')
    n, edges, constraints = load_polyg(polyg_filename)

    print('\ninitializing...')
    timings = {}
    start = time.time()
    enc = Encoding(n)
    init_done = time.time()
    timings['init'] = init_done - start
    print("init: {:.6f}sec".format(timings['init']))

    # TODO: write to file (and time it),
    # probably need a distinction for timing write to file!
    print('\nbuilding encoding...')
    encode_type = 'encode'

    if output_filename:
        encode_type = 'encode_and_write'
        enc.encode(edges, constraints, outfile=output_filename, save_to_file=True)
        # currently not going to be supporting SMT2 output for all encodings
    else:
        enc.encode(edges, constraints)

    encode_done = time.time()
    timings[encode_type] = encode_done - init_done
    print("encode: {:.6f}sec".format(timings[encode_type]))

    print('\nsolving encoding...')
    result = enc.solve()
    solve_done = time.time()
    timings['solve'] = solve_done - encode_done
    print("solve: {:.6f}sec".format(timings['solve']))

    print("\nsat? " + str(result))

    return (result, enc, timings)

def encoding_help(encodings):
    acc = []
    for cl in encodings:
        acc += [' ‣ ', cl.name, ': ', cl.description, '\n']
    return ''.join(acc)

def main():
    helptext = encoding_help(ENCODING_CLASSES)
    parser = argparse.ArgumentParser(description=helptext, formatter_class=RawDescriptionHelpFormatter)
    encoding_choices = {}

    for cl in ENCODING_CLASSES:
        if not cl.name in encoding_choices:
            encoding_choices[cl.name] = cl
        else:
            raise Exception('duplicate encoding names')

    parser.add_argument('encoding', choices=encoding_choices, help='encoding to solve with')
    parser.add_argument('polygraph', help='polygraph file')
    parser.add_argument('-o', '--output', help='save encoding to file')

    args = parser.parse_args()
    encoding = encoding_choices[args.encoding]
    if args.output and not encoding.filetype:
        print('error: that encoding cannot output to file')
        exit(1)
    else:
        run_encoding(encoding, args.polygraph, args.output)
        exit(0)

if __name__ == '__main__':
    main()
