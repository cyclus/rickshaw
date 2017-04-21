"""Main entry point for rickshaw"""
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint
import os
import json
from argparse import ArgumentParser

from rickshaw import generate


def main(args=None):
    p = ArgumentParser('rickshaw')
    p.add_argument('-n', dest='n', type=int, help='number of files to generate',
                   default=None)
    p.add_argument('-i', dest='i', type=str, help='name of input file', default=None)
    ns = p.parse_args(args=args)
    
    simspec = {}
    if ns.i is not None:
        try:
            ext = os.path.splitext(ns.i)[1]
            if ext == '.json':
                with open(ns.i) as jf:
                    simspec = json.load(jf)
                    for k,v in simspec['niche_links'].items():
                        simspec['niche_links'][k] = set(v)
                    for k,v in simspec['archetypes'].items():
                        simspec['archetypes'][k] = set(v)
            elif ext == '.py':
                with open(ns.i) as pf:
                    py_str = pf.read()
                    simspec = eval(py_str)
        except:
            pass
            
    spec = generate.SimSpec(simspec)
            
    if ns.n is not None:
        i = 0
        while i < ns.n:
            try:
                input_file = generate.generate(sim_spec=spec)
            except Exception:
                continue
            jsonfile = str(i) + '.json'
            with open(jsonfile, 'w') as jf:
                json.dump(input_file, jf, indent=4)
            i += 1
    else:
        input_file = generate.generate(sim_spec=spec)
        pprint(input_file)


if __name__ == '__main__':
    main()
