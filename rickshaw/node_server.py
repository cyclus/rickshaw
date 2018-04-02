"""Asynchonous job creation for rickshaw for use on HPC systems."""

import json
import asyncio
import concurrent.futures
from asyncio.subprocess import create_subprocess_exec
from argparse import ArgumentParser

from rickshaw.simspec import SimSpec
from rickshaw.generate import generate

def make_parser():
    """Makes the argument parser for the rickshaw node server."""
    p = ArgumentParser("rickshaw-node-server", description="Rickshaw Node Server CLI")
    p.add_argument("--debug", action='store_true', default=False,
                   dest='debug', help="runs the server in debug mode.")
    p.add_argument("-p", "--nproc", type=int, default=1, dest="nproc",
                   help="Number of processes")
    p.add_argument("-s", "--nsim", type=int, default=1, dest="nsim",
                   help="Number of simulations to run")
    p.add_argument("-n", "--name", type=str, default="cyclus", dest="name",
                   help="Node name")
    p.add_argument("-f", "--format", type=str, default="h5", dest="format",
                   help="The format of output file, h5 or sqlite")
    p.add_argument("-i", "--input", type=str, default=None, dest="i",
                   help="Input templating file for Rickshaw")
    return p

async def run_sim(output_q, filename, template):
    try:    
        specific_spec = SimSpec(ni=False) if template is None else SimSpec.from_file(template)    
        input_dict = generate(sim_spec=specific_spec)
        inputfile = json.dumps(input_dict)
        p = await create_subprocess_exec("cyclus", "-o", filename, "-i", inputfile, "-f", "json")
        await p.wait()
    finally:    
        await output_q.put(filename)

async def run_sims(output_q, nsim, template):
    i = 0
    pending_tasks = []
    while i < nsim:
        while not output_q.empty() and i < nsim:
            filename = await output_q.get()
            sim_task = asyncio.ensure_future(run_sim(output_q, filename, template))
            pending_tasks.append(sim_task)            
            i += 1
        if len(pending_tasks) > 0:
            done, pending_tasks = await asyncio.wait(pending_tasks, return_when=concurrent.futures.FIRST_COMPLETED)
            pending_tasks = list(pending_tasks)
    if len(pending_tasks) > 0:    
        await asyncio.wait(pending_tasks)

def main(args=None):
    p = make_parser()
    ns = p.parse_args(args=args)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=ns.nproc)
    loop = asyncio.get_event_loop()
    output_q = asyncio.Queue()
    for i in range(ns.nproc):
        output_q.put_nowait("{name}-{i:03}.{format}".format(name=ns.name, i=i, format=ns.format))
    if ns.debug:
        loop.set_debug(True)
    try:
        loop.run_until_complete(run_sims(output_q, ns.nsim, ns.i))
    finally:
        if not loop.is_closed():
            loop.close()

if __name__ == '__main__':
    main()
