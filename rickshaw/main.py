"""Main entry point for rickshaw"""
import sys
import os
import subprocess
import json
import logging
import traceback
from argparse import ArgumentParser
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint

from rickshaw import simspec
from rickshaw import generate
from rickshaw import server_scheduler
from rickshaw import blue_waters
from rickshaw import deploy
from rickshaw.generate import CYCLUS_EXECUTABLE

def make_parser():
    p = ArgumentParser('rickshaw')
    p.add_argument('-n', dest='n', type=int, help='number of files to generate',
                   default=None)
    p.add_argument('-i', dest='i', type=str, help='name of input file', default=None)
    p.add_argument('-rs', dest='rs', action="store_true", help='runs the simulations after they have been generated with sqlite')
    p.add_argument('-rh', dest='rh', action="store_true", help='runs the simulations after they have been generated with hdf5')
    p.add_argument('-v', dest='v', action="store_true", help='verbose mode will pretty print generated files')
    p.add_argument('-o', dest='o', type=str, help='name of output file', default='rickshaw')
    p.add_argument('-s', dest='s', type=int, help='run in service mode with s sims', default=None)
    p.add_argument('-op', dest='op', type=str, help='name of cyclus input file without extension', default="rickshaw")
    p.add_argument('-bn', dest='bn', type=int, help='number of nodes to run on if ran on blue waters', default=None)
    p.add_argument('-ppn', dest='ppn', type=int, help='number of processors per node for a blue waters run', default=None)
    p.add_argument('-d', dest = 'd', action="store_true", help='Build a deploy schedule to match the input file')
    return p

def run(specific_spec, ns, name):
    try:
        input_file = generate.generate(sim_spec=specific_spec)
    except Exception as e:
        message = traceback.format_exc()
        logging.exception(message)
    if ns.v:
        pprint(input_file)
    jsonfile = name + '.json'
    try:
        with open(jsonfile, 'w') as jf:
            json.dump(input_file, jf, indent=4)
    except Exception as e:
        message = traceback.format_exc()
        logging.exception(message)
    try:
        if ns.rs:
            cmd = [CYCLUS_EXECUTABLE[:], jsonfile, '-o', ns.o +'.sqlite']
            logging.info(' '.join(cmd))
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, 
                                                universal_newlines=True)
        if ns.rh:
            cmd = [CYCLUS_EXECUTABLE[:], jsonfile, '-o', ns.o +'.h5']
            logging.info(' '.join(cmd))
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, 
                                                universal_newlines=True)
            logging.info(out)
    except Exception as e:
        message = traceback.format_exc()
        message += e.stdout
        logging.exception(message)

def main(args=None):
    p = make_parser()
    ns = p.parse_args(args=args)
    input_file = ""
    if ns.i is not None:
        try:
            specific_spec = simspec.SimSpec.from_file(ns.i)
        except Exception:
            print('Simspec failed to build', file=sys.stderr)
    else:
        specific_spec = simspec.SimSpec()
    if ns.d:
        deploy.run_deploy(ns.n, specific_spec)
        return
    if ns.bn is not None:
        blue_waters.generate_scripts(ns.n, ns.ppn)
    if ns.s is not None:
        ss = server_scheduler.ServerScheduler()
        i = 0        
        while i < ss.ncpu-2:
            ss.start_rickshaw_service(ns.s, i)
            i+= 1
        return     
    if ns.n is not None:
        i = 0
        while i < ns.n:
            run(specific_spec, ns, i)
            i += 1
    else:
        run(specific_spec, ns, ns.op)


if __name__ == '__main__':
    main()
