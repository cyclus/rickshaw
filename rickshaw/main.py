"""Main entry point for rickshaw"""
from argparse import ArgumentParser
import os
import subprocess
import json
import logging
import traceback

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

def main(args=None):
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
    ns = p.parse_args(args=args)
    spec = {}
    input_file = ""
    if ns.i is not None:
        try:
            ext = os.path.splitext(ns.i)[1]
            if ext == '.json':
                with open(ns.i) as jf:
                    spec = json.load(jf)
                    for k,v in simspec['niche_links'].items():
                        spec['niche_links'][k] = set(v)
                    for k,v in simspec['archetypes'].items():
                        spec['archetypes'][k] = set(v)
            elif ext == '.py':
                with open(ns.i) as pf:
                    py_str = pf.read()
                    spec = eval(py_str)
        except:
            print('Failed to parse richshaw input file, please verify file format')
            pass
    if ns.d:
        i = 0;
        min_diff = 1.0
        tempfile = {}
        parameters = {}
        while i < ns.n:
            try:
                specific_spec = simspec.SimSpec(spec)
            except Exception:
                print('Simspec failed to build')
            try:            
                input_file = generate.generate(sim_spec=specific_spec)
                if ns.v:
                    pprint(input_file)
                jsonfile = str(i) + '.json'
                diff = deploy.test_schedule(input_file, spec['parameters'])
                if diff < min_diff:
                    min_diff = diff
                    tempfile = input_file
                    parameters = spec['parameters']
                if diff < 0.05:
                    with open(jsonfile, 'w') as jf:
                        json.dump(input_file, jf, indent=4)
            except Exception as e:
                message = traceback.format_exc()
                logging.exception(message)
            i+=1
        with open('best.json', 'w') as jf:
            json.dump(tempfile, jf, indent=4)
        print('Best schedule match had a difference of: ' + str(min_diff)) 
        deploy.plot_total_power(tempfile, parameters)
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
            try:
                specific_spec = simspec.SimSpec(spec)
            except Exception:
                print('Simspec failed to build')
            try:            
                input_file = generate.generate(sim_spec=specific_spec)
                if ns.v:
                    pprint(input_file)
                jsonfile = str(i) + '.json'
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
            i += 1
    else:
        try:
            specific_spec = simspec.SimSpec(spec)
            input_file = generate.generate(sim_spec=specific_spec)
        except Exception as e:
            message = traceback.format_exc()
            logging.exception(message)
        if ns.v:
            pprint(input_file)
        jsonfile = ns.op + '.json'
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
            logging.exception(message)


if __name__ == '__main__':
    main()
