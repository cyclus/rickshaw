"""Main entry point for rickshaw"""
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint
import json
from argparse import ArgumentParser

from rickshaw import generate


def main(args=None):
    p = ArgumentParser('rickshaw')
    p.add_argument('-n', dest='n', type=int, help='number of files to generate',
                   default=None)
    ns = p.parse_args(args=args)

    if ns.n is not None:
        i = 0
        while i < ns.n:
            try:
                input_file = generate.generate()
            except Exception:
                continue
            jsonfile = str(i) + '.json'
            with open(jsonfile, 'w') as jf:
                json.dump(input_file, jf, indent=4)
            i += 1
    else:
        input_file = generate.generate()
        pprint(input_file)


if __name__ == '__main__':
    main()
